FROM ubuntu:18.04
ENV TZ=Europe/Kiev
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update && apt install -y texlive-fonts-extra texlive-science latexmk
WORKDIR /app/
ENTRYPOINT ["latexmk", "-pdf", "paper.tex"]
