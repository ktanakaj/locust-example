# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "centos/7"

  # ホストPCとゲストPCのネットワークを構築
  config.vm.network "private_network", type: "dhcp"

  # ゲストPCのポートをホストPCに転送
  config.vm.network "forwarded_port", guest: 8089, host: 8089, host_ip: 'localhost', auto_correct: true

  # ホストPCのこのフォルダをマウント
  config.vm.synced_folder ".", "/vagrant", type: "smb"

  # VM環境設定
  config.vm.provider "hyperv" do |vb|
    vb.cpus = 2
    vb.memory = "3072"
  end
  config.vm.provider "virtualbox" do |vb, override|
    vb.cpus = 2
    vb.memory = "3072"
    override.vm.synced_folder ".", "/vagrant", type: "virtualbox"
  end

  # ゲストPCにansibleをインストールし共有フォルダのプレイブックを実行
  config.vm.provision "ansible_local" do |ansible|
    ansible.playbook = "playbook.yml"
    ansible.provisioning_path = "/vagrant/"
  end

  # DHCPで割り当てられたIPアドレスを表示
  config.vm.provision "shell", run: "always" do |s|
    s.inline = "ip addr"
  end
end
