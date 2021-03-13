FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

WORKDIR /var/www

RUN apk --update add bash nano git curl

RUN apk add --no-cache python3 postgresql-libs

RUN apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev libffi-dev

RUN pip install --upgrade pip

# Rust version 1.14 is required to install cryptography dependency (https://github.com/pyca/cryptography/issues/5776)
ENV PATH="/root/.cargo/bin:${PATH}"

RUN curl https://static.rust-lang.org/rustup/dist/x86_64-unknown-linux-musl/rustup-init --output /tmp/rustup-init \
    && chmod +x /tmp/rustup-init \
    && /tmp/rustup-init -y \
    && pip install --no-cache-dir cryptography \
    && rustup self uninstall -y
# End of Rust installation

RUN git clone https://github.com/likz-dev/gt_fb_backend.git /var/www

RUN pip install -r /var/www/requirements.txt

RUN apk --purge del .build-deps