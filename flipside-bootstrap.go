package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"os/exec"
	"flag"
)

var (
	accessKey = flag.String("accessKey", "", "The AWS access key"),
	secretKey = flag.String("secretKey", "", "The AWS secret key"),
)

func main() {
	err := BootstrapAws(accessKey, secretKey)
	if err != nil {
		log.Fatal(err)
	}
}

// Create Vagrantfile with default content
// Run vagrant up
func BootstrapVagrant() error {
	os.MkdirAll(".flipside/salt/roots", 0755)
	os.MkdirAll(".flipside/salt/pillar", 0755)
	err := ioutil.WriteFile("Vagrantfile", []byte(`# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"

  config.vm.network "forwarded_port", guest: 80, host: 8090

  config.vm.synced_folder ".flipside/salt/roots/", "/srv/salt/"
  config.vm.synced_folder ".flipside/salt/pillar/", "/srv/pillar/"

  config.vm.provision "shell", path: "flipside-provision.py", args: ["--salt-version", "git v2014.7.0", '--no-standalone']

  config.vm.provider "virtualbox" do |vb|
    vb.customize ["modifyvm", :id, "--memory", "1024"]
  end

end`), 0644)
	if err != nil {
		return err
	}
	cmd := exec.Command("vagrant", "up")
	cmd.Stdout = os.Stdout
	err = cmd.Run()
	if err != nil {
		return err
	}
	return nil
}

// Check if aws instance is present
// If not,
// Setup Flipfile to use aws by default?
func BootstrapAws(accessKey, secretKey string) error {
	os.Mkdir(".flipside", 0755)
	os.Chdir(".flipside")
	err := ioutil.WriteFile("master.tf", []byte(`
variable "access_key" {}
variable "secret_key" {}
variable "region" {
    default = "eu-west-1"
}
variable "key_name" {}
variable "key_path" {
    default = "key_file.pem"
}

provider "aws" {
    access_key = "${var.access_key}"
    secret_key = "${var.secret_key}"
    region = "${var.region}"
}

resource "aws_security_group" "default" {
    name = "flipside-elb"
    description = "Used in the flipside terraform"

    ingress {
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port = 80
        to_port = 80
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

resource "aws_instance" "flipside_master" {
    ami = "ami-00b11177"
    instance_type = "t1.micro"

    connection {
      user = "root"
      key_file = "${var.key_path}"
    }

    key_name = "${var.key_name}"
    security_groups = ["${aws_security_group.default.name}"]

    provisioner "local-exec" {
        command = "echo ${aws_instance.flipside_master.public_ip} > master.ip"
    }

    provisioner "remote-exec" {
      script = "../flipside-provision.py"
    }
}

resource "aws_eip" "ip" {
    instance = "${aws_instance.flipside_master.id}"
}

output "ip" {
    value = "${aws_eip.ip.public_ip}"
}`), 0644)
	if err != nil {
		return err
	}
	// TODO generate keypair
	err = ioutil.WriteFile("terraform.tfvars", []byte(fmt.Sprintf(`
access_key = "%s"
secret_key = "%s"
key_name = "%s"
key_path = "%s.pem"`, accessKey, secretKey, "flipside-dev", "flipside-dev")), 0644)
	if err != nil {
		return err
	}
	cmd := exec.Command("terraform", "plan")
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	err = cmd.Run()
	if err != nil {
		return err
	}
	return nil
}
