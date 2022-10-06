from unicodedata import category
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from pathlib import Path

class Logger():
    logger_dict={}
    log_category=set([])
    save_dir=Path('logger_dir')

    def __init__(self,name):
        self.name=name
        self.history=pd.DataFrame()
        self.current_history=pd.DataFrame()
        Logger.logger_dict[self.name] = pd.DataFrame()
        self.epoch=0
        if not Logger.save_dir.exists():
            Logger.save_dir.mkdir()


    def update_category(self):
        Logger.log_category.update(set(self.current_history.columns.to_list()))

    def __call__(self,**kwargs):
        new_row = pd.DataFrame(kwargs,index=[0])
        self.current_history=pd.concat([self.current_history,new_row])

    def __str__(self,r=3):
        output_str=''
        if len(self.current_history)>0:
            avg_epoch = self.get_current_epoch_avg()
            for log_c in avg_epoch.index:
                output_str+= 'avg{}:{} \t'.format(log_c,f'%.{r}f'%avg_epoch[log_c])
            return output_str
        else:
            avg_epoch = self.history[self.history.epoch == self.epoch-1].iloc[-1]
            for log_c in avg_epoch.index:
                output_str+= 'avg{}:{} \t'.format(log_c,f'%.{r}f'%avg_epoch[log_c])
            return output_str

    def get_current_epoch_avg(self):
        return self.current_history.mean()

    def get_last_epoch_avg(self):
        return self.history[self.history.epoch == (self.epoch-1)].mean()

    def get_best_record(self,category='loss',mode='min',unit='epoch'):
        _history = self.history.groupby('epoch').mean() if unit == 'epoch' else self.history
        best_index = _history[category].idxmin() if mode == 'min' else _history[category].idxmax()
        return best_index, _history.iloc[best_index]

    def check_best(self,category='loss',mode='min',unit='epoch'):
        _history = self.history.groupby('epoch').mean() if unit == 'epoch' else self.history
        best_index,best_record = self.get_best_record(category,mode,unit)
        return (len(_history[category])-1)==best_index

    def save_epoch(self):
        self.update_category()
        current_category=self.current_history.columns
        self.current_history['epoch'] = self.epoch
        self.epoch += 1
        self.history =pd.concat([self.history,self.current_history.copy()]) #self.history.append(self.current_history.copy()).reset_index(drop=True)
        self.current_history=pd.DataFrame(columns=current_category)
        Logger.logger_dict[self.name]=self.history

    @property
    def get_logger_names():
        return list(Logger.logger_dict.keys())

    @property
    def get_loggers():
        return Logger.logger_dict

    @staticmethod
    def plot(logger_list=None,show_category=None,figsize=(6.2,3),ylim={},unit='epoch',save=True,filename='logger_history.png'):
        if not logger_list:
            logger_list = Logger.logger_dict.keys()

        if show_category:
            show_category = set(show_category) & Logger.log_category
        else:
            show_category = Logger.log_category
        figers, axs = plt.subplots(1,len(show_category),figsize=(len(show_category)*figsize[0],figsize[1]))
        plt.subplots_adjust(hspace=0.5)
        axs = np.array(axs).flatten()

        for logger_name in logger_list:
            for cidx,c in enumerate(show_category):
                if c in Logger.logger_dict[logger_name].columns:
                    _history=Logger.logger_dict[logger_name]
                    _history = _history.groupby('epoch').mean() if unit == 'epoch' else _history
                    _history = _history.reset_index(drop=True)
                    sns.lineplot(data=_history,x=range(len(_history)),y=c,ax=axs[cidx],label=logger_name).set(title = '{}'.format(c))
                    axs[cidx].legend(loc='upper left')
                    if c in ylim.keys():
                        axs[cidx].set_ylim(ylim[c][0],ylim[c][1])
        if save:
            plt.savefig(Logger.save_dir/filename)
        plt.show()

    def export_logger(filename='logger_history.pkl'):
        path = Logger.save_dir/filename
        with open(path,'wb') as f:
            pickle.dump({'loggers':Logger.logger_dict,
                         'category':Logger.log_category}, f)

    def load_logger(filepath='logger_history.pkl'):
        path = filepath
        with open(path, 'rb') as f:
            load_data=pickle.load(f)
            Logger.logger_dict = load_data['loggers']
            Logger.log_category = load_data['category']



#教學
# check_best(self,category='loss',mode='min',unit='epoch')
# get_best_record(self,category='loss',mode='min',unit='epoch')
# logger.epoch_history['loss'].iloc[-1]
# logger.save_epoch()
# plot(show_category=None,figsize=(6.2,3),ylim=None,unit='epoch')
# logger.set_layer(1)

# 相同layer繪畫再一起(category要一樣)
# 無須設定存入變數種類，直接丟即可
# 可以在plot時設定show_category來選擇顯示參數
# 如果想看iter版本，plot時unit給iter(非epoch)
# save_epoch一定要call才可以畫圖，即使是iter版本
# 要先save_epoch 才能 check_best 以及 get_best_record

#example
# training_logger=Logger('Training')#default 0
# validation_logger=Logger('Validation')#default 0
# all_logger=Logger('All')#default 0
# for i in range(10):
#    for j in range(10):
#        training_logger(acc=np.random.rand(),f1score=np.random.rand())
#        all_logger(acc=np.random.rand(),f1score=np.random.rand())
#        validation_logger(acc=np.random.rand())
#    validation_logger.save_epoch()
#    training_logger.save_epoch()
#    all_logger.save_epoch()
#    validation_logger.check_best(category='acc',mode='max',unit='epoch')

# Logger.load_logger('logger_dir/logger_history.pkl')
# Logger.plot(ylim={'acc':[0,1]})

# Logger.plot(show_category= ['loss','acc'],unit='iter')
# Logger.plot(['Training','All'])
# Logger.export_logger()