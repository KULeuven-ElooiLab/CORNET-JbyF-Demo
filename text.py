import streamlit as st
from io import BytesIO
import matplotlib.pyplot as plt
from st_clickable_images import clickable_images
import base64

def centerImage(pathImage,width,underscript):
    images = []
    
    with open(pathImage, "rb") as image:
            encoded = base64.b64encode(image.read()).decode()
            images.append(f"data:image/jpeg;base64,{encoded}")
    clicked = clickable_images(
                images,
                div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
                img_style={'width':f'{width}'},
            )
    if underscript!='':
        st.markdown(f"<p style='text-align: center; color: grey;'>{underscript}</p>", unsafe_allow_html=True)
    

def render_latex(formula, fontsize=12, dpi=600 ):
    """Renders LaTeX formula into Streamlit."""
    fig = plt.figure()
    text = fig.text(0, 0, '$%s$' % formula, fontsize=fontsize)
    
    fig.savefig(BytesIO(), dpi=dpi)  # triggers rendering

    bbox = text.get_window_extent()
    width, height = bbox.size / float(dpi) +0.05
    # set the size of the fig equal to that of the textbox
    fig.set_size_inches((6.15,height))

    # adjusting the postion of the fig so it is in the middle of the textbox
    dy = (bbox.ymin / float(dpi)) / height
    dx = (1-(width / 6.15))/2 # in percentages
    text.set_position((dx, -dy))

    buffer = BytesIO()
    fig.savefig(buffer, dpi=dpi, format='jpg')
    plt.close(fig)
    
    st.image(buffer)


def intro():

    st.markdown("""
    # Description of the project
    The application of mechanical joining technology in various branches of industry such as 
    automotive engineering, construction and white goods has increased considerably over the 
    last 20 years. In order to ensure further growth of these resource-saving joining processes, 
    new users must be able to design these processes quickly and without extensive process know-how. 
    This goal is pursued in the project proposal described here.
    \n Currently, there are two basic evaluation methods for the design of mechanical joints: 
    on the one hand the evaluation of the joint quality via the geometric characteristics 
    of the joint through cross section analysis and on the other hand the evaluation of 
    the joint via the testing of the strength by destructive testing. In principle, it is 
    known that the geometric characteristics such as interlock or neck thickness are directly 
    related to the strength of the joints but a quantitative correlation for different 
    material thickness combinations has not yet been investigated.
    """)

    centerImage(pathImage='docs/IntroPic.png',width='70%',
            underscript='Visualization of the project goal')

    st.write("""
    \n The aim of the project described here is to enable a prognosis of the joint strength 
    for self-pierce riveting with semi-tubular rivets (SPR-ST) and clinching on the basis of 
    geometrical characteristics of the joints as well as the material properties of the parts 
    to be joined. Data-based algorithms (machine learning) and analytical methods will be 
    investigated as prognosis methods. In this way, large experimental series of tests can be 
    avoided and the mechanical joints can be dimensioned many times faster.
    \n This project objective is achieved by determining the correlations between joint geometry 
    and strength on a large number of material thickness combinations experimentally and by 
    means of numerical simulation. On the basis of this data, learning algorithms can be 
    trained and the analytical methods can be validated in order to achieve the highest possible 
    prediction quality at the end of the project. 
    """)

    
    


def analytical_General():
    st.write('''
    ### General
    Based on several parameters is it possible to analytically predict the strength of the joint. 
    These calculations are divided into two groups depending on the type of failure. From an 
    analytical viewpoint, it is possible to arrive at a solution for a failure that is dominated 
    by i) plastic deformation or ii) fracture. In the literature, various equations have been proposed 
    to predict the strength under the pull-out and the shear tensile loading. Based on 50 
    cases in our database for clinched joints, we defined the best performing analytical predictions. 
    Those four analytical approaches are implemented  this web application. 
    \n To know the strength of the joint in a particular loading condition, you need to calculate 
    the strength associated with  both failure modes. By comparing both the strengths, the lowest 
    strength serves as the predicted strength for the investigated joint configuration and loading condition.  
    ''')

    centerImage(pathImage='docs/Analytical.jpg',width='80%',
            underscript='')

def analytical_howItWorks():
    st.write('''
    ### How it works
    On the left hand side of this web App you have a sidebar where all parameters 
    are located that are needed for the calculations. You can fill those in for 
    one particular case. Or, in case you want to predict the strength for multiple 
    cases, there is also a tool where you upload your excel file. You can download 
    the template below. This excel file can upload to process your data.
    \n A small parameter description and the analytical formulas can be 
    found in the dropdown boxes below, respectively.
    ''')
    with st.expander("Description of the calculation parameter"):
            centerImage(pathImage='docs/Parameter1.jpg',width='70%',
            underscript='Basic parameters that can be measured during a cross section analysis')
            centerImage(pathImage='docs/Parameter2.jpg',width='100%',
            underscript='These are the average stresses taken from the FE-software. Left: Simplification based on tube drawing process with a die angle α. Right: Combination of tube and rod drawing ')
            

    with st.expander("Description of the formulas"):
            
            analytical_TT()
            analytical_ST()

def analytical_TT():
    

    st.write('''
    #### Top tensile test
    The deformation process during a top tensile test resembles a  **tube sinking process without a mandrel**. 
    This implies that the die-side sheet can be seen as a rigid ‘die’. The most basic formula applies when 
    the clinch is simplified to a tube.  However, it is known that this is an oversimplification resulting 
    in a underestimation of the maximum strength. According to Coppieters et al. [[1]](https://www.sciencedirect.com/science/article/pii/S0263823111002679?casa_token=B9vJYddxRZwAAAAA:5qLzJcUV4gLqi2gJPE3CC38byUndCJ8UfmIoVFduI26Dy3b0XCoLJw55gXLHm4FdiM2AsEBYMekKXg), 
    the bottom part of the clinch contributes to the strength as it is radially compressed when assuming 
    a rigid die. In this project, however, some deficiencies of the model proposed in [[1]](https://www.sciencedirect.com/science/article/pii/S0263823111002679?casa_token=B9vJYddxRZwAAAAA:5qLzJcUV4gLqi2gJPE3CC38byUndCJ8UfmIoVFduI26Dy3b0XCoLJw55gXLHm4FdiM2AsEBYMekKXg) were eliminated. 
    The improvement lies in a better definition of the basic shapes (tube and rod) that enter the analytical 
    calculation. In this web App, those shapes are defined by means of the geometrical parameters of the 
    clinching joint. It shown that this enhances the predictive accuracy of the analytical prediction as 
    reported in [[1]](https://www.sciencedirect.com/science/article/pii/S0263823111002679?casa_token=B9vJYddxRZwAAAAA:5qLzJcUV4gLqi2gJPE3CC38byUndCJ8UfmIoVFduI26Dy3b0XCoLJw55gXLHm4FdiM2AsEBYMekKXg).
    This method is semi analytic due to the fact that the stress needs to be obtained from the FE-model (see 'Description of the calculation parameter'). 
    > *The maximum top tensile force of deformation-dominant failure is calculated according to the improved approach based on Coppieters et al. [[1]](https://www.sciencedirect.com/science/article/pii/S0263823111002679?casa_token=B9vJYddxRZwAAAAA:5qLzJcUV4gLqi2gJPE3CC38byUndCJ8UfmIoVFduI26Dy3b0XCoLJw55gXLHm4FdiM2AsEBYMekKXg)*
    ''')

    
    
    render_latex(r"F_{def} = {A_n\left[-\frac{4\pi}{\sqrt{3}}\sigma_{yield}^{Tube}\left(\frac{1+\beta}{\omega}\right)+\left(\frac{A^{Rod}_{exit}\sigma^{Rod}_{yield}\left(\frac{1+\beta}{\beta}\right)\left[1-\left(\frac{A^{Rod}_{exit}}{A^{Rod}_{entry}}\right)^{\beta}\right]}{A^{Tube}_{entry}}+\frac{4\pi}{\sqrt{3}}\sigma_{yield}^{Tube}\left(\frac{1+\beta}{\omega}\right)\right)\left(\frac{A^{Tube}_{entry}}{A_n}\right)^{\frac{\omega}{2\pi}}\right]}")

    # render_latex(r"F_{def} = {A_{n,tube}\left[\frac{2}{\sqrt{3}}\sigma_{yield}^{Tube}\left(\frac{1+\beta}{\beta}\right)+\left(\frac{A^{Rod}_{exit}\sigma^{Rod}_{yield}\left(\frac{1+\beta}{\beta}\right)\left[1-\left(\frac{A^{Rod}_{exit}}{A_f}\right)^{\beta}\right]}{A^{Tube}_{entry}}-\frac{2}{\sqrt{3}}\sigma_{yield}^{Tube}\left(\frac{1+\beta}{\beta}\right)\right)\left(\frac{A_{n,tube}}{A^{Tube}_{entry}}\right)^{\beta}\right]}")
    st.write('''
    The top sheet is the thinnest in the neck region meaning that the joint will fracture in this region. 
    This failure mode resembles a uniaxial tensile test on a tubular specimen with a thickness equal to 
    the neck thickness  [[2]](https://www.sciencedirect.com/science/article/pii/S0261306909006220). 
    This calculation is fully analytical when the area is derived from experimental data.
    > *The fracture strength can be calculated as follows:*
    ''')
    render_latex(r'''F_{frac} = A_n\sigma_{UTS}''')
    
def analytical_ST():
    st.write('''
    #### Shear lap tensile test
    When applying a shear load to a single lap shear specimen, a complex deformation of 
    the joint and sheets will occur. The most simplified representation is a tube under 
    shear loading. Due to the large deformation and associated strain hardening of the sheets 
    during clinching, the local yield stress has increased. Therefore, numerical data is 
    needed to determine the yield stress after joining (AFS)(see 'Description of the calculation parameter'). The strength for a deformation-dominated 
    failure can be computed using:
    ''')
    render_latex(r'''F_{def} = A_n\frac{\sigma_{AFS}}{\sqrt{3}}''')
    st.write('''
    An empirical method was used to calculate the strength until fracture [[3]](https://op.europa.eu/nl/publication-detail/-/publication/98b4398c-7df1-4f03-9b14-f753aa063532). 
    ''')
    render_latex(r'''F_{frac} = \frac{t_1\alpha}{4}(2d+\alpha t_1)\pi\sigma_{UTS} \quad with: \quad \alpha=0.4''')
    
def results(strengthTT,modeTT,strengthST,modeST):
    st.write(f'''
    Based on the manual input for the clinching joint under investigation, the analytical analysis predicts a joint  failure at 
    **{strengthTT}** during **top tensile load** where failure is dominated by {modeTT}. 
    During a **shear load** we predict that the joint can withstand **{strengthST}** with {modeST} as dominant failure mode. 
    \n The results of all four analytical calculations can be seen in the table below. 
    ''')

def  Machine_General():
    st.write('''
    ## Strength prognosis based on machine learning
    ### General
    * 	Use the menu on the left to alter the input parameters
    *   The corresponding dimensions will be illustrated on the figure below        
    * 	After changing a parameter, the strength is automatically recalculated
    ### Summary of the input variables
    ''')

    centerImage(pathImage='docs/ML1.jpg',width='65%',
            underscript='')

def WF_experiments():
    st.write('''
    ### General
    The first step towards the data-driven strength prognosis of a clinch joint is collecting experimental data. 
    This data is then used for the validation of finite element (FE) simulations as well as for increasing the 
    prognosis quality of the data-based algorithm. Based on four materials (three steel and one aluminium grade) 
    with a minimum of three different sheet thicknesses, a statistical test plan with 73 material combinations 
    was created for the experimental  campaign.
    ### Experimental data of the joint
    In order to validate the stress state within the material, the force-displacement curve was measured during 
    the joining process. To take this into account during the machine learning process, the maximum setting 
    force was used as an input value.
    ''')

    centerImage(pathImage='docs/ProcessCurve.jpg',width='40%',
            underscript='A typical process curve of the clinching process with a maximum setting force of 43 kN.')

    st.write('''
    The typical geometrical parameters were also measured via a cross-section analysis. These parameters were 
    used for the validating the simulations  and as input values for the machine learning process. 
    The experimental cross-section was used to tune the frictional parameters in the FE model used to simulated the joining process. 
    ''')
    
    centerImage(pathImage='docs/CrossSection-M.png',width='60%',
            underscript='The contour of the clinch with the measurments of the geometrical parameters.')

    st.write('''
    ### Experimental data of the joint strength
    For assessing the joint strength, two different loading conditions were used, namely the pull-out 
    (also referred to as the top tensile test) and the shear lap test. It must be noted that only the 
    maximum force during the experiments (joint strength) was used in further steps.
    ''')
    centerImage(pathImage='docs/StrengthTests.jpg',width='80%',
            underscript='Two loading conditions used for the determination of the max force. Left: Pull-out Right: Shear lap')

def WF_simulations():
    st.write('''
    ### General
    For the strength prediction with the help of data-based algorithms, a large database is required. This is possible 
    with only experimental data, but this would be costly and labor intensive. Therefore, in the second step, 
    we replicate the experiments using a FE-software called 
    [Simufact forming](https://www.simufact.com/simufactforming-forming-simulation.html). In this project, 
    our aim was to find a trade-off between computational effort and predictive accuracy of the FEM 
    considering the three simulation steps (joining, pull-out and shear lap testing). Through existing features 
    within this software, it was possible to automate the results transfer from the joining simulation to the strength 
    test. Which decreased the total conversion time drastically.
    ### Simulation
    Before we can calculate the strength of the joint with the FE-software, the material must be characterized and 
    a friction model must be selected. It was shown in a previous project [[1]](https://cornet.efb.de/general-description-flow-curve-jbyf.html ) that the clinching forming simulation 
    is most accurate when measuring the flow curve using the stack compression test. Consequently, all 
    flow curves in this project are determined using the stack compression test. The combined friction method is an appropriate model 
    for mechanical joining simulations. It is shown that this frictional 
    model enables to accurately simulate the metal flow during joining. The governing parameters of the 
    combined friction model were individually tuned for all 73 cases.
    ''')

    centerImage(pathImage='docs/Simulation-Strategy.jpg',width='70%',
            underscript='Simulation strategy,starting with the joining on the left side and import the result into the strength tests on the right side.')

    st.write('''
    For the simulation of the joining process (see below) and the pull-out test, an axisymmetric (2D) 
    model was used to reduce computational time. The results of the joining process were automatically 
    imported into the strength simulation and subsequently revolved for the shear lap test, which requires a 3D simulation.
    ### Results
    For each simulation step, a deviation between the experiment was calculated. Based on the average 
    deviation of those steps, 50 out of 73 cases were selected for the next step. The latter elimination 
    was required to improve the accuracy of the virtual database.
    ''')

    centerImage(pathImage='docs/ResultsSimulation.jpg',width='70%',
            underscript='Deviation between the numerical and experimental data of the 50 best simulations')

def WF_DoE():
    st.write('''
    ### General
    From the 73 experiments, we selected the 50 most accurate simulations. With this database is it 
    possible to train some basic machine learning algorithms. However, it must be emphasized that 
    once you use more advanced models, there is obviously a need for more data. To achieve a larger 
    database, variations are made on the 50 most accurate simulations. With the help of these virtual 
    experiments, we can lower the cost and save resources. By making several parameters variable, you 
    rapidly end up with a large amount of variations. Therefore, we firstly perform a Design of 
    Experiments (DoE) to select 20 variations without losing the overall response of all possible combinations. 
    In the function tab above, you can create your own DoE. Because we are working in a virtual environment, 
    variations on the joining tools are cheaper to obtain.      
    ''')

    centerImage(pathImage='docs/Principle_DoE.jpg',width='70%',
            underscript='Data acquisition on the basis of the validated database. Going from 50 joints upto 1000 with DoE.')

    st.write('''
    ### Variable parameters
    The parameter variations  are chosen based on their  influence on the geometrical parameters and strength of the joint. 		
    > * Material property: Scaling the flow curve with 10 and 20%. Hereby, investigating the response of stronger material combinations.
    > * Process parameter: Scaling the bottom thickness tb up to 15%.
    > * Tool geometry: the parameters shown in the figure below are considered as variables.
    ''')
    centerImage(pathImage='docs/VariedParameters.jpg',width='50%',
            underscript='The tool geometry is discribed with these parameters and are varied over a dicreet or continu interval.')

def WF_MachineLearning():
    st.write('''
    Under construction
    ''')

def WF_function_DoE():
    st.write('''
    ### How it works
    With this function is it possible to do your own design of experiments. With the help of the Latin 
    hypercube sampling method, a certain amount of samples can be taken from the larger matrix with all 
    possible combinations. To do the DoE, follow the steps below
    >   1.	Fill in the names of the parameters that you want to vary. There must be at least two variables.
    >   2.	Open the sidebar by pressing on the **>** in the top left corner. 
    >   3.	Select the amount of samples that you want to take.
    >   4.	Define each parameter: discreet or continue and the boundaries for each of the parameter
    >   5.	Download the DoE under the visualization of the first 2 variables.
    ''')

def WF_function_ML_Train():
    emptycol1,col,emptycol2=st.columns([1,6,1])
    st.write('''
    ### How it works
    This function makes it possible to train six different regression algorithms. Before using this 
    function, we recommend you to read the machine learning tab first. This will give you 
    more insight concerning  the working and workflow of machine learning. With this function 
    is it possible to train and save your best model for each algorithm and output variable. 
    This is possible after completing the following steps:
    ''')
    with st.expander("1.    Define the database:"):
        st.write('''
        By default, the database of the project is used. There is also the possibility to upload 
        your own database. Simply upload your file and select uploaded in the drop down menu.
        ''')
    
    with st.expander("2.	Define the in- and output:"):
        st.write('''
        Start with selecting the output variables that you want to predict. By pressing on the button 
        **‘Transfer remaining variables to input’**, all remaining names transfer to the drop down menu on 
        the right. Delete the variables that you don’t need. Once you select **‘Set the in- & output’**, 
        a visualization of the database is created with the colors for the in- and output. Press **‘Yes’** 
        to continue with these settings.
        ''')
    
    with st.expander("3.	Select an algorithm:"):
        st.write('''
        Here, you can chose from six regression algorithms. Some are more advanced than 
        others. And therefore, the more advanced will have more hyperparameters and will 
        take longer to train. At this point, if you don’t want to tune the hyperparameters, 
        you can start training a model with the basic settings **(go to step 6)**.
        ''')
    
    with st.expander("4.	Select the hyperparameters that you want the change:"):
        st.write('''
        To improve the predictive accuracy of the algorithm, it is possible to tune the hyperparameters. 
        If you hover over the **‘?’**, a short description is given for that hyperparameter. Select the ones 
        you want to change and press **‘Start tuning …’**
        ''')
    
    with st.expander("5.	Define the boundaries of the hyperparameters:"):
        st.write('''
        With the use of a grid search, all possible combinations of hyperparameters will be considered. 
        Consequently, training time will increase drastically when you increase the possible values of 
        the hyperparameters. Based on the type of the hyperparameter, different boundaries will be 
        defined. For an integer or float, a min and max boundary needs to be defined. Also a value 
        **‘#’** dividing the interval in that amount of equal parts. The bigger this value, the more time 
        it will take to train the model. Press **‘Start to train’** when all boundaries are defined.
        ''')
    
    with st.expander("6.	Train the model:"):
        st.write('''
        Because the algorithm can only be trained for one specific output variable at once, 
        this needs to be selected. Now, select **‘Train’** and wait until a table and graph is plotted. 
        In the table can all possible combinations be found with their r²-value. In the most right 
        column, you can rearrange the table based on their rank. This can help to tune the 
        hyperparameters even more. In the graph, the prediction against the measured value 
        can be seen for the best (ranked as number 1) hyper settings. Once you are satisfied 
        with the result, press on **‘Download the trained model’**. This will download the best 
        model for that particular algorithm, hyperparameters and output variable. With this 
        file is it now possible to go to the function **ML-Predicting**.
        ''')

    st.write('''
    ### Start training
    ''')

def WF_function_ML_Predict():
    st.write('''
    ### How it works
    Before you can do your prediction, a machine learning model needs to be trained. This 
    can be done in the function tab ML-training. Once you have this, upload this file below 
    this text. Now, two options can be selected in the sidebar:
    >   **1.	Manual:** Based on the input variables of the model, input fields are created in the sidebar. With this method, a fast prediction can be made for one case.

    >   **2.	Excel:**  Based on the input variables of the model, a template (csv file) with the correct column tags can be downloaded. Complete this with your data and save this an excel file. After you upload this file, the predictions can be downloaded.
    ''')
