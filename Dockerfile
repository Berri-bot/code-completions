FROM python:3.10-slim

# Set environment variables
ENV JAVA_VERSION=21.0.2
ENV JDT_VERSION=1.36.0
ENV JDT_BUILD=202406030953
ENV JAVA_HOME=/app/lsp/java/jdk-${JAVA_VERSION}
ENV JDT_HOME=/app/lsp/java/jdt-language-server-${JDT_VERSION}
ENV WORKSPACE_DIR=/app/workspace

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    maven \
    curl \
    tar \
    unzip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install JDK
RUN mkdir -p /app/lsp/java && \
    cd /app/lsp/java && \
    curl -L "https://download.oracle.com/java/21/archive/jdk-${JAVA_VERSION}_linux-x64_bin.tar.gz" \
    -H "Cookie: oraclelicense=accept-securebackup-cookie" | tar -xz

# Install JDT Language Server
RUN mkdir -p ${JDT_HOME} && \
    curl -L -o /tmp/jdtls.tar.gz \
    "https://download.eclipse.org/jdtls/milestones/${JDT_VERSION}/jdt-language-server-${JDT_VERSION}-${JDT_BUILD}.tar.gz" && \
    tar -xzf /tmp/jdtls.tar.gz -C ${JDT_HOME} --strip-components=1 && \
    rm /tmp/jdtls.tar.gz

# Create workspace and logs directory
RUN mkdir -p ${WORKSPACE_DIR} /app/logs && \
    chmod -R 777 ${WORKSPACE_DIR} /app/logs

# Verify installation
RUN ${JAVA_HOME}/bin/java -version && \
    ls -la ${JDT_HOME}/plugins

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt "uvicorn[standard]" "python-lsp-server[all]"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]