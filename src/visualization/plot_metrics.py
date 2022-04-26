import pandas as pd
import matplotlib.pyplot as plt
import os

output_directory = 'output/'
decay = 'decay_iter_10k/'
fix = 'FIX_iter_10k/'
output_decay = [file for file in os.listdir(output_directory+decay) if file.endswith('.csv')]
output_fix = [file for file in os.listdir(output_directory+fix) if file.endswith('.csv')]
# print(output_fix)

for idx, file in enumerate(output_decay):
    df_fix = pd.read_csv(output_directory+fix+file)
    df_decay = pd.read_csv(output_directory+decay+file)
    ad = pd.DataFrame.merge(df_fix, df_decay,
                        on=['Step'],
                        how='inner',
                        suffixes=('_fix', '_decay'))
    ad.rename({'Value_decay':'weight_decay',
            'Value_fix':'weight_fix'},
            axis=1,
            inplace=True)
    if f"{file.replace('run-.-tag-', '').replace('.csv', '')}" != 'lr' and f"{file.replace('run-.-tag-', '').replace('.csv', '')}"  != 'total_loss':
        ad['weight_decay'] = ad['weight_decay']/100
        ad['weight_fix'] = ad['weight_fix']/100
    print(ad.head())

    ax = plt.gca() 
    ad.plot(kind = 'line',
            y = 'weight_decay',
            x = 'Step',
            color = 'cornflowerblue', ax=ax)
    ad.plot(kind = 'line',
            y = 'weight_fix',
            x = 'Step',
            color = 'coral', ax=ax)
    if f"{file.replace('run-.-tag-', '').replace('.csv', '')}" == 'lr':
        plt.ylabel("learning rate", fontsize=10)
    else:
        plt.ylabel(f"{file.replace('run-.-tag-', '').replace('.csv', '')}", fontsize=10)
    # plt.title(f"{file.replace('run-.-tag-', '').replace('.csv', '')}")
    plt.xlabel('Iteration', fontsize=10)
    plt.grid()
    plt.savefig(f"{output_directory}graph/{file.replace('run-.-tag-', '').replace('.csv', '')}.png")
    plt.clf()
    # plt.show()


# df_fix = pd.read_csv(output_directory+fix+'run-.-tag-bbox_AP.csv')
# df_decay = pd.read_csv(output_directory+decay+'run-.-tag-bbox_AP.csv')
# ad = pd.DataFrame.merge(df_fix, df_decay,
#                     on=['Step'],
#                     how='inner',
#                     suffixes=('_fix', '_decay'))

# ad.drop(columns=['Wall time_fix', 'Wall time_decay'], inplace=True)
# ad.rename({'Value_decay':'weight_decay',
#             'Value_fix':'weight_fix'},
#             axis=1,
#             inplace=True)
# print(ad.head())

# ax = plt.gca() 
# ad.plot(kind='line',
#         x='Step',
#         y='weight_decay',
#         color = 'coral',
#         ax=ax)
# ad.plot(kind='line',
#         x='Step',
#         y='weight_fix',
#         color = 'cornflowerblue',
#         ax=ax)
# plt.grid()
# plt.show()