## A mini-program for volunteer activity management
[![Build Status](https://travis-ci.com/jameslahm/volunteers-tsinghua.svg?token=zMepxcNDKbRfwzCYs7iz&branch=master)](https://travis-ci.com/jameslahm/volunteers-tsinghua)

[![codecov](https://codecov.io/gh/jameslahm/volunteers-tsinghua/branch/web/graph/badge.svg?token=sxCNZSRWjU)](https://codecov.io/gh/jameslahm/volunteers-tsinghua)

- Run:
  - DEPLOY:
    ```bash
    cd webapp
    sudo docker-compose up
    ```
  - PC: 
    ```bash
    cd webapp
    make init_db
    make runserver
    ```
  - WX:
    ```bash
    cd wxapp && npm run build
    ```

- Test:
  ```bash
  cd webapp && make test
  ```

- Init database:
  ```bash
  cd webapp && make init
  ```

- Migrate database:
  ```bash
  cd webapp && make migrate
  ```

- Upgrade:
  ```bash
  cd webapp && make upgrade
  ```


