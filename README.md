### Mongodb Web Client

#### build

```bash
docker build . -t mongo_ui:$(cat .version)
```

#### run

```bash
docker-compose up -d
```

TODO:
- [ ] ext.xxx.xxx query