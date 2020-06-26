FROM python

RUN curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh --output miniconda.sh
RUN bash miniconda.sh -b -p $HOME/miniconda

RUN eval "$($HOME/miniconda/bin/conda shell.bash hook)" \
    && conda init \
    && conda create --name simple-server -y \
    && conda activate simple-server \
    && conda install -y flask \
    && conda install -y pandas

WORKDIR /gorila
COPY . .

EXPOSE 5000

CMD eval "$($HOME/miniconda/bin/conda shell.bash hook)" \
    && conda activate simple-server \
    && python app.py
