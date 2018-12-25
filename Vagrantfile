# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/bionic64"

  # ホストPCとゲストPCのネットワークを構築
  config.vm.network "private_network", type: "dhcp"

  # ゲストPCのポートをホストPCに転送
  config.vm.network "forwarded_port", guest: 8089, host: 8089, host_ip: 'localhost', auto_correct: true

  # ホストPCのこのフォルダをマウント
  config.vm.synced_folder ".", "/vagrant", type: "virtualbox"

  # CPU数/メモリサイズ
  config.vm.provider "virtualbox" do |vb|
      vb.cpus = 2
      vb.memory = "3072"
  end

  # ゲストPCにansibleをインストールし共有フォルダのプレイブックを実行
  config.vm.provision "ansible_local" do |ansible|
    ansible.playbook = "playbook.yml"
    ansible.provisioning_path = "/vagrant/"
  end
end
