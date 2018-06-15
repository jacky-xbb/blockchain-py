# blockchain-py


This is a python imlementation of [blockchain_go](https://github.com/Jeiwan/blockchain_go)


## Usage
### Create a wallet
> python cli.py createwallet
Your new address: LYKpRRQozyCCjMvD8fYXZbqjNb4GTX5w93

### Create blockchain and receive first mining reward
>  python cli.py createblockchain --address LYKpRRQozyCCjMvD8fYXZbqjNb4GTX5w93

### Get balance of some address
>  python cli.py getbalance --address LYKpRRQozyCCjMvD8fYXZbqjNb4GTX5w93 

### Create another wallet
> python cli.py createwallet
Your new address: LYJbecz4ynDcGieqXVUMfSXXAwkCaou4oa

### Send coins to someone
> python cli.py send --from LYKpRRQozyCCjMvD8fYXZbqjNb4GTX5w93 --to LYJbecz4ynDcGieqXVUMfSXXAwkCaou4oa --amount 6

### Print blockchain information
> python cli.py print

***

**Todo**

- [x] [Basic Prototype](https://jeiwan.cc/posts/building-blockchain-in-go-part-1/)
- [x] [Proof-of-Work](https://jeiwan.cc/posts/building-blockchain-in-go-part-2/)
- [x] [Persistence and CLI](https://jeiwan.cc/posts/building-blockchain-in-go-part-3/)
- [x] [Transactions 1](https://jeiwan.cc/posts/building-blockchain-in-go-part-4/)
- [x] [Addresses](https://jeiwan.cc/posts/building-blockchain-in-go-part-5/)
- [ ] [Transactions 2](https://jeiwan.cc/posts/building-blockchain-in-go-part-6/)
- [ ] [Network](https://jeiwan.cc/posts/building-blockchain-in-go-part-7/)


[教程中文翻译](https://github.com/liuchengxu/blockchain-tutorial/blob/master/content/SUMMARY.md)

Thanks to [liuchengxu](https://github.com/liuchengxu)
