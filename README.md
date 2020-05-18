### Mongodb Web Client

#### build

```bash
docker build . -t mongo_ui:$(cat .version)
```

#### run

```bash
docker-compose up -d
```

#### doc

![main](doc/main.png)

![single-query](doc/single-query.png)

![multi-query](doc/multi-query.png)

TODO:
- [X] ext.xxx.xxx query
- [ ] selected field table view