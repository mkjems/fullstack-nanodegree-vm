
#Tournament Results

This is my submission to the Udacity Full Stack Developer course 'Tournament Results' project.

## Requirements

[Virtualbox](https://www.virtualbox.org/) and [Vagrant](http://vagrantup.com/)

## How to run the code

First clone the virtual machine. Start it up and ssh into it.

	git clone git@github.com:mkjems/fullstack-nanodegree-vm.git
	cd fullstack-nanodegree-vm/vagrant/
	vagrant up
	vagrant ssh

Once you are in

	cd /vagrant/tournament
	make test
	make test-basic
	make simulation
	make clean
	make clean-test

## Features

 - The tests pass!
 - The code will prevent rematches
 - You can run a simulation of a 16 player tournament

