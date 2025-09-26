#!/bin/bash
version=$1       
full_version=$2  


if [ -z "$version" ] || [ -z "$full_version" ] ; then
    echo "Usage: $0 <major_version> <full_version>"
    echo "Example: $0 23 23.0.2 x64"
    exit 1
fi

JAVA_DIR="/usr/local/java"
JDK_TAR="jdk-${full_version}_linux-x64_bin.tar.gz"
JDK_URL="https://download.oracle.com/java/${version}/archive/${JDK_TAR}"
sudo mkdir -p "$JAVA_DIR"

wget -q --show-progress "$JDK_URL" -O "$JDK_TAR"
sudo tar -xzf "$JDK_TAR" -C "$JAVA_DIR"

JDK_FOLDER=$(tar -tf "$JDK_TAR" | head -1 | cut -f1 -d"/")
echo "export JAVA_HOME=${JAVA_DIR}/${JDK_FOLDER}" | sudo tee /etc/profile.d/java.sh > /dev/null
echo 'export PATH=$JAVA_HOME/bin:$PATH' | sudo tee -a /etc/profile.d/java.sh > /dev/null

source /etc/profile.d/java.sh
java -version

