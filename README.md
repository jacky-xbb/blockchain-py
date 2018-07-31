

# blockchain-py


This is a python imlementation of [blockchain_go](https://github.com/Jeiwan/blockchain_go)


## Usage
### Create a wallet
```bash
$ python cli.py createwallet
Your new address: 17Y288D5DnFwU6cj5M8YHnxYNnDhN6f5FK
```

### Create blockchain and receive first mining reward
```bash
$ python cli.py createblockchain --address 17Y288D5DnFwU6cj5M8YHnxYNnDhN6f5FK
```

### Create another wallet
```bash
$ python cli.py createwallet
Your new address: 15zBUPbr2B4JMcQHg6oJ8DYQi4t7RN1gWb
```

### Send coins to someone
```bash
$ python cli.py send --from 17Y288D5DnFwU6cj5M8YHnxYNnDhN6f5FK --to 15zBUPbr2B4JMcQHg6oJ8DYQi4t7RN1gWb --amount 6
Mining a new block
0005ec56906edfcc97a8b422cd6948e7a2b59cba89e9a253f75eeefb6755d6e9


Success!
```

### Get balance of some address
```bash
$ python cli.py getbalance --address 17Y288D5DnFwU6cj5M8YHnxYNnDhN6f5FK 
Balance of 17Y288D5DnFwU6cj5M8YHnxYNnDhN6f5FK
```

***

**Todo**

- [x] [Basic Prototype](https://jeiwan.cc/posts/building-blockchain-in-go-part-1/)
- [x] [Proof-of-Work](https://jeiwan.cc/posts/building-blockchain-in-go-part-2/)
- [x] [Persistence and CLI](https://jeiwan.cc/posts/building-blockchain-in-go-part-3/)
- [x] [Transactions 1](https://jeiwan.cc/posts/building-blockchain-in-go-part-4/)
- [x] [Addresses](https://jeiwan.cc/posts/building-blockchain-in-go-part-5/)
- [x] [Transactions 2](https://jeiwan.cc/posts/building-blockchain-in-go-part-6/)
- [ ] [Network](https://jeiwan.cc/posts/building-blockchain-in-go-part-7/)


[教程中文翻译](https://github.com/liuchengxu/blockchain-tutorial/blob/master/content/SUMMARY.md)

Thanks to [liuchengxu](https://github.com/liuchengxu)
