from math import fabs
from tkinter import DISABLED
from requests import session
import streamlit as st
import hydralit_components as hc 
from streamlit_tags import st_tags,st_tags_sidebar
from pyDOE import lhs
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FixedLocator, FixedFormatter
from sklearn.linear_model import LinearRegression, HuberRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import QuantileTransformer
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score, make_scorer
from PIL import Image


def experimenten():
    st.markdown('## Experimental setup')
    st.image(Image.open('docs/Exp_setup.png'))

def simulerenExperimenten():
    st.markdown('## Deviation between the numerical and experimental data of the 50 best simulations')
    st.image(Image.open('docs/Simuleren_results.png'))

def DoE():
    st.markdown('DoE')

def OpbouwDatabase():
    st.markdown('Opbouwen database')

def ML():
    
    st.markdown('ML')

def feature_DoE():
    def transform(listvar,continuity, colomLHS,col):
        i=0
        if continuity == 'continu':
            interval= listvar[1]-listvar[0]
            while i < colomLHS.shape[0]:
                x[i,col]=listvar[0]+interval*x[i,col]
                i+=1
        elif continuity == 'discreet':
            while i < colomLHS.shape[0]:
                for j in range(len(listvar)):
                    if(x[i,col]>(j/len(listvar))) and (x[i,col]<=((j+1)/len(listvar))):
                        x[i,column]=listvar[j]
                i+=1
    list_var = []

    # define the variables with there names
    keywords = st_tags(
    label='# Enter Keywords:',
    text='Press enter to add more',
    value=[],
    key="1")
    
    # do the latin hypercube sampling 
    column = 0
    samp = int(st.sidebar.number_input('How many samples do you want to pick?',min_value=1))
    x = lhs(len(keywords),samples=samp,criterion="center")
    

    # Define the interval of each variable
    for key in keywords:
        list_temp=[]
        list_temp.append(key)
        st.sidebar.markdown(f"# {key}")
        list_temp.append(st.sidebar.radio(f"How to vary {key}",('discreet','continu')))

        if list_temp[1]=='continu':
            Var = st_tags_sidebar(
            label=f'Enter values for the variable: {key}',
            text='Press enter to add more',
            maxtags=2,
            key=key)
            
            list_temp.append(list(map(float, Var)))
        elif list_temp[1]=='discreet':
            Var = st_tags_sidebar(
            label=f'Enter values for the variable: {key}',
            text='Press enter to add more',
            key=key)

            list_temp.append(list(map(float, Var)))

        # list with name, discreet/continu, interval
        list_var.append(list_temp)

    # display the charters for 2 values
    try:
        # display the fundamental charter of LHS
        fig, axs = plt.subplots(1,2,figsize=(9, 4))
        for i in range(samp-1):
            axs[0].axvline(x=(i+1)/samp, color='grey')
            axs[0].axhline(y=(i+1)/samp, color='grey')
            axs[0].plot(x[:, 0], x[:, 1], "o")
        axs[0].set_xlabel(f"x1 ({list_var[0][0]})")
        axs[0].set_ylabel(f"x2 ({list_var[1][0]})")
        axs[0].set_xlim(xmin = 0, xmax = 1)
        axs[0].set_ylim(ymin = 0, ymax = 1)


        # display the final charter after the transformation
        while column < x.shape[1]:
            transform(list_var[column][2],list_var[column][1],x[:,column],column)
            column+=1
        axs[1].scatter(x[:,0],x[:,1])
        axs[1].set_xlabel(list_var[0][0])
        axs[1].set_ylabel(list_var[1][0])
        print(list_var[0][2])
        if list_var[0][1]== "discreet":
            axs[1].xaxis.set_major_locator(FixedLocator(list_var[0][2]))
            plt.setp(axs[1].get_xticklabels(), rotation=45, horizontalalignment='right')
        if list_var[1][1]== "discreet":
            axs[1].yaxis.set_major_locator(FixedLocator(list_var[1][2]))
        st.pyplot(fig)
    
        # import al the data into de dictionary 'val'
        val={}
        for j in range(len(keywords)):
            temp = []
            for i in range(samp):
                temp.append(x[i][j])
            val[keywords[j]]=temp
        
        # add the results to the dataframe
        df = pd.DataFrame.from_dict(val)

        # Make it posible to download the results as csv file
            # file_name = st.text_input('Name the file', "Strength_predictions")
        st.download_button('Download the DoE', df.to_csv(sep = ';',index=False,decimal=','), file_name = "Your_own_DoE" + ".csv")
    except:
        st.warning('A minimum of 2 vaiables need to be assigned')

def feature_ML_Train():
    #All the algorithms that can be chosen. Add here your algorithm if you want
    def get_algorithm(alg): 
        'LinearRegression','HuberRegressor','SVR','KNeighborsRegressor','GradientBoostingRegressor','MLPRegressor'
        if alg == 'LinearRegression': return LinearRegression()
        if alg == 'HuberRegressor': return HuberRegressor()
        if alg == 'SVR': return SVR()
        if alg == 'KNeighborsRegressor': return KNeighborsRegressor()
        if alg == 'GradientBoostingRegressor': return GradientBoostingRegressor()
        if alg == 'MLPRegressor': return MLPRegressor()
    
    # get the info over the hyperparameter from the perticular algorithm
    def getInfoParameter(algorithm, parameter,settings): 
        def find(str, ch):
            for i, ltr in enumerate(str):
                if ltr == ch:
                    yield i

        text = algorithm.__doc__
        startPoints = []
        for param in algorithm.get_params().keys():
            startPoints.append(text.find(param+' :'))
        startPoints.append(text.find('Attributes\n'))
        startPoints.sort()
        indexStartPoint = startPoints.index(text.find(parameter+' :'))
        infoParameter = text[startPoints[indexStartPoint]:startPoints[indexStartPoint+1]]
        if settings == False: #get the describtion of the specific hyperparameter
            return infoParameter
        else: #get the default values or the list with all possible settings for this specific hyperparameter
            infoParamSettings = infoParameter[infoParameter.find(':')+2:infoParameter.find('default')-2].removesuffix(' or callable' or ', greater than 1')
            list_settings = []
            if '{' in infoParamSettings:
                setting= []
                for i in list(find(infoParamSettings, "'")):
                    setting.append(i)
                    if len(setting)==2:
                        list_settings.append(setting)
                        setting = []
                for indexSettingsArray in range(len(list_settings)):
                    list_settings[indexSettingsArray]=infoParamSettings[list_settings[indexSettingsArray][0]+1:list_settings[indexSettingsArray][1]]
                if ('float' or 'int') in infoParamSettings:
                    list_settings.append(infoParamSettings[infoParamSettings.find('or')+3:])
                return list_settings
            else:
                return infoParamSettings

    # define the variables that can be saved during in the memory
    if 'Input' not in st.session_state:
        st.session_state['Input'] = False
    if 'ready for training' not in st.session_state:
        st.session_state['ready for training']=False

    # select the database that you want to use for the training
    databases = {"synthetic (n=712)": "docs\TrainDatabase_712.xlsx"}
    col1, col2 = st.columns(2)
    uploadedFile  = col2.file_uploader("Import the excel with all your data",type=["xlsx","csv"])
    if uploadedFile:
        databases["uploaded"]=uploadedFile
    database = col1.selectbox("Select database",databases.keys())
    data = pd.read_excel(databases[database])
    
    

    with st.expander('Select the in and output',expanded=True).form('Select in and out put variables'):
        
        col1,col2 = st.columns(2)
        col1.markdown('### Output')
        col2.markdown('### Input')
        output_color = col1.color_picker('Pick A Color', '#ADD8E6')
        input_color = col2.color_picker('Pick A Color', '#90EE90')

        
        
        # based on the name of the columns can the output variables be selected 
        output_variables =  col1.multiselect(" ",
            list(data.columns))
        # If the button is clicked, all remaining variables are set as input
        if st.form_submit_button("Transfer remaining variables to input",help="Unless the output variables remained the same"):
            st.session_state["Input"]=False
        # it is possible to delete some input variables
        if output_variables!=[]:
                
            input_variables =  col2.multiselect('',
                    [x for x in list(data.columns) if x not in output_variables],[x for x in list(data.columns) if x not in output_variables])
        else:
            input_variables =  col2.multiselect(' ',
                    [])
            st.session_state["Input"]=False
        if output_variables and input_variables !=[]:
            if st.form_submit_button("Set the in- & output"):
                st.session_state["Input"]=False
                st.write('Are the input correct?')
                st.dataframe(data.head().style.set_properties(**{'subset':output_variables,'background-color': output_color})\
                                    .set_properties(**{'subset':input_variables,'background-color': input_color})    )
                col3,col4 = st.columns(2)
                
                col3.form_submit_button("Yes")
                        # X = data[input_variables]
                        # y=data[output_variables] #.values.ravel() for machine learning
                col4.form_submit_button("No")
    
    X = data[input_variables]
    y=data[output_variables]
    
    
    try: test = st.session_state["FormSubmitter:Select in and out put variables-Yes"]
    except: test = False
    if test or st.session_state["Input"]:
        
        st.session_state["Input"]=True
        col1,col2 = st.columns(2)
        
        with col1.expander('Select the algorithms'):
            algorithm = st.radio('Select the algorithm',('LinearRegression','HuberRegressor','SVR','KNeighborsRegressor','GradientBoostingRegressor','MLPRegressor'))
                # [LinearRegression(),HuberRegressor(),SVR(),KNeighborsRegressor(),GradientBoostingRegressor(),MLPRegressor()]
            algorithm = get_algorithm(algorithm)


        with col2.expander('Select the hyperparameters that you want the change').form('Select algorithms'):
                list_hyper_checked = []
                list_hyperpara = []
                list_parameters = []
                
                for parameters in algorithm.get_params().keys():
                    list_hyper_checked.append(st.checkbox(parameters,help=getInfoParameter(algorithm,parameters,settings=False)))
                    list_hyperpara.append(parameters)
                if st.form_submit_button(f'selecteer de hyperparameters voor {algorithm} '):
                    if True in list_hyper_checked:
                        st.session_state['ready for training']=False
                    else:
                        st.session_state['ready for training']=True
                for i in range(len(list_hyper_checked)):
                        if list_hyper_checked[i]==True:
                            para = list_hyperpara[i]
                

                
                            iniPara = []
                            iniPara.append('model__' + para)
                            for x in range(2):
                                if algorithm.get_params()[para]==None:
                                    iniPara.append(-1)
                                else:
                                    iniPara.append(algorithm.get_params()[para])
                            iniPara.append(1)
                            iniPara.append(getInfoParameter(algorithm,para,settings=True))
                            list_parameters.append(iniPara)
                


        my_dict={}    
        if list_parameters != []:
            with st.form('define hyperpara'):
                st.write('Define the boundaries of the hyperparameters')
                for x in range(len(list_parameters)):
                    list_settings = []
                    with st.expander(list_parameters[x][0][7:]):
                        if isinstance(list_parameters[x][4], list):
                            for i in range(len(list_parameters[x][4])):
                                if list_parameters[x][1] in list_parameters[x][4][i]:
                                    if st.checkbox(list_parameters[x][4][i],True,key = x*10+i):
                                        list_settings.append(list_parameters[x][4][i])
                                else:
                                    if st.checkbox(list_parameters[x][4][i],key = x*10+i):
                                        list_settings.append(list_parameters[x][4][i])
                            
                            if 'float' in list_settings:
                                    list_settings = []
                                    statments = ["Start", "Stop", "#"]
                                    col1,col2,col3 = st.columns(3)
                                    if list_parameters[x][1] != float:
                                        list_parameters[x][1]=1
                                        list_parameters[x][2]=1

                                    list_parameters[x][1] = float(col1.text_input(statments[0],list_parameters[x][1],key = x*10+1))
                                    list_parameters[x][2] = float(col2.text_input(statments[1],list_parameters[x][2],key = x*10+2))
                                    list_parameters[x][3] = int(col3.text_input(statments[2],list_parameters[x][3],key = x*10+3))
                                    st.warning('Only float will be selected even if other options are checked')
                            else:
                                list_parameters[x][1]=list_settings
                            



                        elif list_parameters[x][4] =='bool':
                            list_bool = ['True','False']
                            for i in range(len(list_bool)):
                                if str(list_parameters[x][1]) in list_bool[i]:
                                    if st.checkbox(list_bool[i],True,key = x*10+i):
                                        list_settings.append(eval(list_bool[i]))
                                else:
                                    if st.checkbox(list_bool[i],key = x*10+i):
                                        list_settings.append(eval(list_bool[i]))
                            list_parameters[x][1]=list_settings
                        else:
                            statments = ["Start", "Stop", "#"]
                            col1,col2,col3 = st.columns(3)
                            if 'float' in list_parameters[x][4]:
                                list_parameters[x][1] = float(col1.text_input(statments[0],list_parameters[x][1],key = x*10+1))
                                list_parameters[x][2] = float(col2.text_input(statments[1],list_parameters[x][2],key = x*10+2))
                            else:
                                try:
                                    list_parameters[x][1] = int(col1.text_input(statments[0],list_parameters[x][1],key = x*10+1))
                                    list_parameters[x][2] = int(col2.text_input(statments[1],list_parameters[x][2],key = x*10+2))
                                except:
                                    st.error('The input value must be an integer.')
                            list_parameters[x][3] = int(col3.text_input(statments[2],list_parameters[x][3],key = x*10+3))
                       # st.write(list_parameters) 
                ready_to_train = st.form_submit_button("Start to train")
                            
                            
    
                
            for w in range(len(list_parameters)):
                    x=[]
                    if isinstance(list_parameters[w][1],list):
                        my_dict[list_parameters[w][0]] = list_parameters[w][1]
                    elif list_parameters[w][4]=='int':
                        for v in np.linspace(list_parameters[w][1],list_parameters[w][2],list_parameters[w][3]):
                            x.append(int(v))
                        my_dict[list_parameters[w][0]] = x
                    else:
                        for v in np.linspace(list_parameters[w][1],list_parameters[w][2],list_parameters[w][3]):
                            x.append(v)
                        my_dict[list_parameters[w][0]] = x
            
            
        
        try:replacement = ready_to_train
        except: replacement =False
        
        if st.session_state['ready for training'] or replacement:
                    st.session_state['ready for training']=True
                # if my_dict != {}:
                    train_with = st.selectbox('On what output do you want to train',y.keys())
                            
                            
                    if st.button('Train'):
                        pipe =Pipeline([
                        ("scale", QuantileTransformer(n_quantiles=int(len(X)*0.66))),
                        ("model", algorithm)])
                        
                        model = GridSearchCV(pipe,
                            my_dict,
                            scoring={'R^2':make_scorer(r2_score)},
                            refit='R^2',
                            n_jobs=-1,
                            cv=3,
                            verbose = 2)
                        
                        print(model.fit(X,y[train_with].values.ravel()).verbose)
                        
                        st.dataframe(model.cv_results_)
                        
                        y_predict = model.best_estimator_.predict(X)
                        st.write(model.best_estimator_)

                        def plot_regression_results(ax, y_true, y_pred, title, scores):
                            """Scatter plot of the predicted vs true targets."""
                            ax.plot(
                                [y_true.min(), y_true.max()], [y_true.min(), y_true.max()], "--r", linewidth=2
                            )
                            ax.scatter(y_true, y_pred, alpha=0.2)
                            ax.get_xaxis().tick_bottom()
                            ax.get_yaxis().tick_left()   
                            ax.set_xlim([y_true.min(), y_true.max()])
                            ax.set_ylim([y_pred.min(), y_pred.max()])
                            ax.set_xlabel("Measured")
                            ax.set_ylabel("Predicted")
                            extra = plt.Rectangle(
                                (0, 0), 0, 0, fc="w", fill=False, edgecolor="none", linewidth=0
                            )
                            ax.legend([extra], [scores], loc="upper left")
                            ax.set_title(title)
                        
                        fig, ax = plt.subplots()

                        plot_regression_results(
                        ax,
                        y[train_with],
                        y_predict,
                        train_with,
                        (r"$R^2={:.2f} \pm {:.2f}$").format(
                            model.cv_results_["mean_test_R^2"][model.best_index_],
                            model.cv_results_["std_test_R^2"][model.best_index_]
                        ))
                        st.pyplot(fig)
                        
    st.button('nothing')
  
def feature_ML_Predict():
    print('doing nothing')

def show_page():
    # Navigationbar
    menu_data = [
        {'label':"Experimenten"},
        {'label':"Simuleren"},
        {'label':"Design of Experiment (DoE)"},
        {'label':"Opbouwen database"},
        {'label':"Machine Learning (ML)"},
        {'label':"Functions",'submenu':[{'label':"DoE"},{'label':"ML-Training"},{'label':"ML-Predicting"}]}]

    over_theme = {'txc_inactive': '#00000','menu_background':'white','txc_active': 'red', }
    menu_id = hc.nav_bar(    
        menu_definition=menu_data,
        first_select= int(10),
        override_theme=over_theme,
        home_name='Home',
        hide_streamlit_markers=True, #will show the st hamburger as well as the navbar now!
        sticky_nav=True, #at the top or not
        sticky_mode='sticky', #jumpy or not-jumpy, but sticky or pinned
            )
    
    # start a def based on the selected tab in the navigationbar
    if menu_id == "Experimenten":
            experimenten()
    if menu_id == "Simuleren":
        simulerenExperimenten()
    if menu_id == "Design of Experiment (DoE)":
            DoE()
    if menu_id == "Opbouwen database":
            OpbouwDatabase()
    if menu_id == "Machine Learning (ML)":
            ML()
    if menu_id == "DoE":
            feature_DoE()
    if menu_id == "ML-Training":
        feature_ML_Train()
    if menu_id == "ML-Predicting":
        feature_ML_Predict()
    if menu_id == "Home":
        return 3
    return 2