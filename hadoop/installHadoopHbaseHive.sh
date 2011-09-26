#!/bin/bash -eua

ABS_PATH=$(cd ${0%/*} && echo $PWD/${0##*/})
ROOT=$(dirname "$ABS_PATH")
DOWNLOAD_DIR=$ROOT/download
TARGET_DIR=$ROOT/software
JAVA_HOME="/Library/Java/Home"
CLEANUP="ALL" #ALL|SOFTWARE|NONE
#hadoop config
HADOOP_VERSION="hadoop-0.20.203.0"
HADOOP_URL="http://ftp.wayne.edu/apache//hadoop/common/${HADOOP_VERSION}/${HADOOP_VERSION}rc1.tar.gz"
#hive config
HIVE_VERSION="hive-0.7.1"
HIVE_URL="http://mirror.candidhosting.com/pub/apache//hive/stable/${HIVE_VERSION}.tar.gz"
#hbase config
HBASE_VERSION="hbase-0.90.4"
HBASE_URL="http://www.takeyellow.com/apachemirror//hbase/stable/${HBASE_VERSION}.tar.gz"
HBASE_ROOTDIR="$TARGET_DIR/$HBASE_VERSION/rootdir"

function cleanup {
    echo "======================Cleanup====================================="
    mkdir -p $DOWNLOAD_DIR
    mkdir -p $TARGET_DIR
    if [ $CLEANUP="ALL" ]; then
        rm -rf $DOWNLOAD_DIR/*
        rm -rf $TARGET_DIR/*
    elif [ $CLEANUP="SOFTWARE" ]; then
        rm -rf $DOWNLOAD_DIR/*
    fi
    echo "======================Done: Cleanup====================================="
}

function changeHadoopConfig {
    HADOOP_HOME=$TARGET_DIR/$HADOOP_VERSION
    sed -i -e "s%.*export JAVA_HOME.*%export JAVA_HOME=${JAVA_HOME}%g" $HADOOP_HOME/conf/hadoop-env.sh
    cp $ROOT/conf/core-site.xml $HADOOP_HOME/conf/
    cp $ROOT/conf/hdfs-site.xml $HADOOP_HOME/conf/
    cp $ROOT/conf/mapred-site.xml $HADOOP_HOME/conf/
}

function setupPassphraseless {
    ssh-keygen -t dsa -P '' -f ~/.ssh/id_dsa
    cat ~/.ssh/id_dsa.pub >> ~/.ssh/authorized_keys
}


function installHadoop {
    echo "======================Install Hadoop====================================="
    cd $TARGET_DIR
    if [ ! -f ${DOWNLOAD_DIR}/${HADOOP_VERSION}.tar.gz ]; then
        curl $HADOOP_URL --O ${DOWNLOAD_DIR}/${HADOOP_VERSION}.tar.gz
    fi

    tar -xvzf ${DOWNLOAD_DIR}/${HADOOP_VERSION}.tar.gz
    export HADOOP_HOME=$TARGET_DIR/$HADOOP_VERSION
    cd $HADOOP_HOME
    changeHadoopConfig
    echo "======================Done: Install Hadoop====================================="
}

function installHive {
    echo "======================Install Hive====================================="
    cd $TARGET_DIR
    if [ ! -f ${DOWNLOAD_DIR}/${HIVE_VERSION}.tar.gz ]; then
        curl $HIVE_URL --O ${DOWNLOAD_DIR}/${HIVE_VERSION}.tar.gz
    fi

    tar -xvzf ${DOWNLOAD_DIR}/${HIVE_VERSION}.tar.gz
    export HIVE_HOME=$TARGET_DIR/$HIVE_VERSION
    export PATH=$HIVE_HOME/bin:$PATH
    echo "======================Done: Install Hive====================================="
}

function changeHbaseConfig {
    HBASE_HOME=$TARGET_DIR/$HBASE_VERSION
    cp $ROOT/conf/hbase-site.xml $HBASE_HOME/conf/
    sed -i -e "s%<value>.*</value>%<value>$HBASE_ROOTDIR</value>%g" $HBASE_HOME/conf/hbase-site.xml
}

function installHBase {
    echo "======================Install HBase====================================="
    cd $TARGET_DIR
    if [ ! -f ${DOWNLOAD_DIR}/${HBASE_VERSION}.tar.gz ]; then
        curl $HBASE_URL --O ${DOWNLOAD_DIR}/${HBASE_VERSION}.tar.gz
    fi

    tar -xvzf ${DOWNLOAD_DIR}/${HBASE_VERSION}.tar.gz
    export HBASE_HOME=$TARGET_DIR/$HBASE_VERSION
    changeHbaseConfig
    echo "======================Done: Install Hadoop====================================="
}

function echoHadoopUsage {
    echo "============================Hadoop Usage=========================="
    echo "To start hadoop: $HADOOP_HOME/bin/start-all.sh"
    echo "Hit NameNode at http://localhost:50070/"
    echo "Hit JobTracker - http://localhost:50030/"
    echo "Stop deamon: $HADOOP_HOME/bin/stop-all.sh"
    echo "Format FS: $HADOOP_HOME/bin/hadoop namenode -format"
    echo "============================Example=========================="
    echo "Copy the input files into the distributed filesystem:"
    echo "$ $HADOOP_HOME/bin/hadoop fs -put conf input"
    echo "Run some of the examples provided:"
    echo "$ $HADOOP_HOME/bin/hadoop jar hadoop-*-examples.jar grep input output 'dfs[a-z.]+'"
    echo "Examine the output files:"
    echo "$ $HADOOP_HOME/bin/hadoop fs -get output output "
    echo "$ cat output/*"
    echo "Or"
    echo "$ $HADOOP_HOME/bin/hadoop fs -cat output/*"
    echo "======================Done: Hadoop Usage====================================="
}

function echoHbaseUsage {
    echo "============================HBase Usage=========================="
    echo "To start hbase: $HBASE_HOME/bin/start-hbase.sh"
    echo "To stop hbase: $HBASE_HOME/bin/stop-hbase.sh"
    echo "To start hbase shell: $HBASE_HOME/bin/hbase shell"
    echo "Sample create: create 'test', 'cf'"
    echo "Sample insert: put 'test', 'row1', 'cf:a', 'value1'"
    echo "Sampel list: scan 'test'"
    echo "Sampel query: get 'test', 'row1'"
    echo "Sample delete: disable 'test'; drop 'test'"
    echo "======================Done: HBase Usage====================================="
}

cleanup
installHadoop
installHBase
echoHadoopUsage
echoHbaseUsage
