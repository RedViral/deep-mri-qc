import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

from sklearn.metrics import roc_curve, roc_auc_score

import imageio


def make_roc_gif(results_dir, epochs, fold_num=1):
    images = []

    epoch_range = range(1, epochs+1)
    for epoch in epoch_range:
        filename = results_dir + 'ROC_fold_' + str(fold_num) + '_epoch_' + str(epoch) + '.png'
        img = plt.imread(filename)
        images.append(img)

    imageio.mimsave(results_dir + 'ROC_fold_' + str(fold_num) + '.gif', images)


def plot_roc(train_truth, train_probs, val_truth, val_probs, test_truth, test_probs, results_dir, epoch_num, fold_num=-1):
    plt.figure(figsize=(8, 8))

    lw = 2
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')

    try:
        train_roc_auc = roc_auc_score(train_truth, train_probs[:, 1], 'weighted')
        train_fpr, train_tpr, _ = roc_curve(train_truth, train_probs[:, 1])
        plt.plot(train_fpr, train_tpr, color='darkorange', lw=lw, label='Train ROC (area = %0.2f)' % train_roc_auc)
    except:
        print('Couldnt plot training')

    try:
        val_roc_auc = roc_auc_score(val_truth, val_probs[:, 1], 'weighted')
        val_fpr, val_tpr, _ = roc_curve(val_truth, val_probs[:, 1])
        plt.plot(val_fpr, val_tpr, color='red', lw=lw, label='Val ROC (area = %0.2f)' % val_roc_auc)
    except:
        print('Couldnt plot validation')

    try:
        test_roc_auc = roc_auc_score(test_truth, test_probs[:, 1], 'weighted')
        test_fpr, test_tpr, _ = roc_curve(test_truth, test_probs[:, 1])
        plt.plot(test_fpr, test_tpr, color='darkred', lw=lw, label='Test ROC (area = %0.2f)' % test_roc_auc)
    except:
        print('Couldnt plot test')

    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate', fontsize=20)
    plt.ylabel('True Positive Rate', fontsize=20)
    plt.title('ROC Epoch:' + str(epoch_num), fontsize=24)
    plt.legend(loc="lower right", shadow=True, fontsize=20)

    plt.savefig(results_dir + 'ROC_fold_' + str(fold_num) + '_epoch_' + str(epoch_num) +  '.png', bbox_inches='tight')
    plt.close()

def plot_sens_spec(train_sens, train_spec, val_sens, val_spec, test_sens, test_spec, results_dir, fold_num=-1):
    plt.figure(figsize=(8, 8))

    epoch_number = range(len(train_sens))

    lw = 2

    if not train_sens is None:
        plt.plot(epoch_number, train_sens, color='darkorange', lw=lw, label='Train Sensitivity')
    if not train_spec is None:
        plt.plot(epoch_number, train_spec, color='gold', lw=lw, label='Train Specificity')


    if not val_sens is None:
        plt.plot(epoch_number, val_sens, color='darkred', lw=lw, label='Validation Sensitivity')
    if not val_spec is None:
        plt.plot(epoch_number, val_spec, color='salmon', lw=lw, label='Validation Specificity')

    if not test_sens is None:
        plt.plot(epoch_number, test_sens, color='darkblue', lw=lw, label='Test Sensitivity')
    if not test_spec is None:
        plt.plot(epoch_number, test_spec, color='mediumblue', lw=lw, label='Test Specificity')

    plt.legend(shadow=True, fontsize=20)
    plt.savefig(results_dir + 'results_fold_' + str(fold_num), bbox_inches='tight')
    plt.close()

