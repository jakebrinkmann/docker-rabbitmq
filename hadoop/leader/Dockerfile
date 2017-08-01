FROM centos:7
RUN yum upgrade -y \
    && yum install -y wget which

# Install Java ===========================
WORKDIR /usr/local/
RUN wget --no-cookies \
    --no-check-certificate \
    --header "Cookie: oraclelicense=accept-securebackup-cookie" \
    "http://download.oracle.com/otn-pub/java/jdk/7u55-b13/jdk-7u55-linux-x64.tar.gz" \
    -O jdk-7-linux-x64.tar.gz \
    && tar zvxf jdk-7-linux-x64.tar.gz \
    && rm jdk-7-linux-x64.tar.gz
    
ENV JAVA_HOME "/usr/local/jdk1.7.0_55"
ENV PATH "$PATH:$JAVA_HOME/bin"

# Install Hadoop =========================
RUN wget https://archive.apache.org/dist/hadoop/common/hadoop-2.4.1/hadoop-2.4.1.tar.gz \
    && tar xvzf hadoop-2.4.1.tar.gz \ 
    && rm hadoop-2.4.1.tar.gz
    
ENV HADOOP_HOME "/usr/local/hadoop-2.4.1"
ENV PATH "$PATH:$HADOOP_HOME/bin"

