# 書式：　FROM [イメージ] [タグ]
$ FROM　Flask:3.0.3

# 書式：　RUN [コマンド]
$ RUN apt update \
&& apt install -y apache2

# 書式：　CMD ["実行ファイル", "パラメータ1","パラメータ2"]
$ CMD ["apachectl","-D","FOREGROUND"]

# 書式：　COPY [コピー元][コピー先]
$ COPY　index.html /mydir/index.html
$ COPY　index.html　/mydir/
$ COPY src/ /mydir/

# 書式：　WORKDIR [ディレクトリのパス]
$ WORKDIR /app
