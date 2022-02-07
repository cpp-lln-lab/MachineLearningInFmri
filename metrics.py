import numpy as np
import pandas as pd
from savingOutputs import save_dicts


def compute_metric(filename, subjects_ids, metric, mode, ret = False):
    confusion_matrixes = pd.read_csv(filename+"confusion_matrixes_"+mode+".csv", index_col=0)
    masks_exist = pd.read_csv(filename+"masks_exist.csv", index_col=0)
    score = [dict() for _ in subjects_ids] 
    for modality in confusion_matrixes:
        for i, subj_id in enumerate(subjects_ids):
            if masks_exist[modality][subj_id] :
                cf = confusion_matrixes[modality][subj_id].replace("[","").replace("]","").replace("\n","")
                if mode == "within" : cf = cf.split('.')[:-1]
                else : cf = [i for i in cf.split(' ') if i != '']
                cf = np.asarray(list(map(int, cf))).reshape(4,4)
                score[i][modality] = metric["function"](cf)
    save_dicts(filename + metric["name"] +"_" + mode + ".csv", score, list(score[0].keys()), subjects_ids)
    if ret : return score


def compute_accuracy_bootstrap(n_subjects, n_single_perm, confusion_matrixes_bootstrap):
    scores = [0]*n_subjects
    for i in range(n_subjects):
        scores[i] = [dict() for _ in range(n_single_perm)]
        for j in range(n_single_perm):
            cfm_bootstrap = confusion_matrixes_bootstrap[i][j]
            for modality in cfm_bootstrap:
                scores[i][j][modality] = accuracy(cfm_bootstrap[modality])
    return scores


def accuracy(confusion_matrix):
    sum_Tis = sum([confusion_matrix[i][i] for i in range(4)])
    return sum_Tis/np.sum(confusion_matrix)


def recall(confusion_matrix):
    recall = [0]*4
    for i in range(4):
        recall[i] = confusion_matrix[i][i]/sum([confusion_matrix[j][i] for j in range(4)])
    return recall


def precision(confusion_matrix):
    precision = [0]*4
    for i in range(4):
        precision[i] = confusion_matrix[i][i]/sum(confusion_matrix[i])
    return precision