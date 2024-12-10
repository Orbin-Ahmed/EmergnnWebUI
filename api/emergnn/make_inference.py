import argparse
from api.emergnn.load_data import DataLoader
import torch
from api.emergnn.base_model import BaseModel
import json
import os

def make_inference(name1, name2):
    print('test')
    drug1, drug2 = name2id(name1, name2)
    if drug1 is None:
        return {'interaction': 'Drug not found', 'interaction_type': 'None'}
    else:
        h, t = drug2id(drug1, drug2)
        if h is None:
            return {'interaction': 'Drug ID not found', 'interaction_type': 'None'}

    # if name2id(name1, name2) is None:
    #     return {'interaction': 'Drug not found', 'interaction_type': 'None'}
    # drug1, drug2 = name2id(name1, name2)
    # if drug2id(drug1, drug2) is None:
    #     return {'interaction': 'Drug ID not found', 'interaction_type': 'None'}
    # h, t = drug2id(drug1, drug2)
    #I've changed a few things in other scripts to make this work on CPU by changing parts that say .cuda() to .to('cpu')
    # parser = argparse.ArgumentParser(description="Parser for EmerGNN")
    # parser.add_argument('--task_dir', type=str, default='./', help='the directory to dataset')
    # parser.add_argument('--dataset', type=str, default='S0', help='the directory to dataset')
    # parser.add_argument('--lamb', type=float, default=7e-4, help='set weight decay value')
    # parser.add_argument('--gpu', type=int, default=-1, help='GPU id to load.')
    # parser.add_argument('--n_dim', type=int, default=128, help='set embedding dimension')
    # parser.add_argument('--save_model', action='store_true', default=False)
    # parser.add_argument('--load_model', default=True, action='store_true') #make this True
    # parser.add_argument('--lr', type=float, default=0.03, help='set learning rate')
    # parser.add_argument('--n_epoch', type=int, default=100, help='number of training epochs')
    # parser.add_argument('--n_batch', type=int, default=512, help='batch size')
    # parser.add_argument('--epoch_per_test', type=int, default=5, help='frequency of testing')
    # parser.add_argument('--test_batch_size', type=int, default=16, help='test batch size')
    # parser.add_argument('--seed', type=int, default=1234)

    # args = parser.parse_args()
    # torch.cuda.set_device(args.gpu)
    # device = torch.device('cpu')
    # dataloader = DataLoader(args)
    # eval_ent, eval_rel = dataloader.eval_ent, dataloader.eval_rel
    # KG = dataloader.KG
    # print(KG)
    # args.all_ent, args.all_rel, args.eval_rel = dataloader.all_ent, dataloader.all_rel, dataloader.eval_rel
    # #for S0 only:
    # args.lr = 0.01
    # args.lamb = 0.000001
    # args.n_dim = 32
    # args.n_batch = 32
    # args.length = 3
    # args.feat = 'E'

        class Args:
            def __init__(self):
                self.task_dir = os.path.abspath('api/emergnn/')
                self.dataset = 'S0'
                self.lamb = 0.000001  # Updated from 7e-4
                self.gpu = -1
                self.n_dim = 32  # Updated from 128
                self.save_model = False
                self.load_model = True
                self.lr = 0.01  # Updated from 0.03
                self.n_epoch = 100
                self.n_batch = 32  # Updated from 512
                self.epoch_per_test = 5
                self.test_batch_size = 16
                self.seed = 1234
                self.length = 3
                self.feat = 'E'
                self.all_ent = None
                self.all_rel = None
                self.eval_rel = None

    args = Args()
    
    device = torch.device('cpu')
    dataloader = DataLoader(args)
    eval_ent, eval_rel = dataloader.eval_ent, dataloader.eval_rel
    KG = dataloader.KG
    print(KG)
    
    args.all_ent = dataloader.all_ent
    args.all_rel = dataloader.all_rel
    args.eval_rel = dataloader.eval_rel

    model = BaseModel(eval_ent, eval_rel, args, entity_vocab=dataloader.id2entity, relation_vocab=dataloader.id2relation)

    triplet_to_test = torch.tensor([h, t])

    pred = model.test_single(triplet_to_test, KG)
    print('Prediction on '+str(triplet_to_test[0]) + ' and '+str(triplet_to_test[1]))

    interaction = ''
    interaction_type=''
    print(pred)
    if 1 in list(pred[0]):
        interaction = 'Yes'
        interaction_type = str(id2relations(pred))
    else:
        interaction='No'
        interaction_type = 'No interaction'

    return {'interaction': interaction, 'interaction_type': interaction_type}

def drug2id(drug1, drug2):
    with open(os.path.abspath('api/emergnn/id2drug.json')) as f:
        id2drug = json.load(f)
    drugs = [drug1, drug2]
    ids = []
    
    for drug in drugs:
        for id, d in id2drug.items():
            for type in d.values():
                if drug==type:

                    ids.append(id)
                    break
               
    if len(ids) != 2:
        return None, None
    
    return int(ids[0]), int(ids[1])

def id2relations(id):
    with open(os.path.abspath('api/emergnn/id2relation.json')) as f:
        id2rel = json.load(f)

    relations = []
    for i, j in enumerate(id[0]):
        if j:
            relations.append(id2rel[str(i)])
    return relations

def name2id(name1, name2):
    with open (os.path.abspath('api/emergnn/name2id.json')) as f:
        name2id=json.load(f)


    name1=name1.lower()
    name2=name2.lower()

    try:
        dbid1 = name2id.get(name1)
        dbid2 = name2id.get(name2)
    except:
        dbid1 = None
        dbid2 = None


    print('ID1')
    print(dbid1)
    print('ID2')
    print(dbid2)
    return dbid1, dbid2
 

