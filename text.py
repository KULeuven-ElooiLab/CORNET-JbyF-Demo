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
    Currently the design of mechanical joining processes like self-pierce riveting with 
    semi-tubular rivet (SPR-ST) and clinching for production is subject to complex and experimental test 
    series in which process parameters such as the rivet or die geometry are varied iteratively and based 
    on experience until a suitable joint contour and strength is achieved. To simplify the use of mechanical 
    joining technologies, these development cycles and thereby the effort for implementation into production must be reduced.
    """)

    centerImage(pathImage='docs/IntroPic.png',width='70%',
            underscript='Basic parameters that can be measured during a cross section analysis')
    

    st.markdown("### Data-based algorithms")
    

    
    st.markdown("""
    ### Analytical formulas
    To predict the strength using analytical formulas, a literature review was done. Papers were found only for 
    clinch joints. When predicting the strength with analytical formulas, it is important to know that there are two dominant 
    failure mechanisms. The first dominant failure mode is fracture in the punch side sheet. The second failure mode is 
    completely dominated by plastic deformation. In this case, the clinch joint will locally deform hereby reducing the 
    interlock between both sheets eventually leading to unbuttoning of the joint. In practice, a combination of both failure modes occurs.
    The predominant failure mode of the clinch is determined by the calculated lower bound strength.
    """)

def analytical_General():
    st.write('''
    ### General
    Based on several parameters is it possible to predict the maximum force that the joint can handel. 
    These calculations are divided into 2 groups of failure. Viz, deformation and fracture dominant 
    failure. In the literature, various equations have been found for both the pull-out and the shear 
    tensile tests. Based on 50 cases, we defined the best performing equations. 
    ''')

    centerImage(pathImage='docs/Analytical.jpg',width='80%',
            underscript='')

    st.write('''
    Those 4 equations are used in this web application. To know the maximum strength of the joint in a 
    particular loading condition, you need to calculate the strength of both failure modes. 
    The lowest calculated force will be the strength of the joint and the condition of failure. 
    ''')

def analytical_howItWorks():
    st.write('''
    ### How it works
    On the left, you have the sidebar with all parameters needed for the calculations. 
    You can fill those in for one particular case. Or, if you want to predict the strength 
    of multiple joints at once, there is also a tool where you upload your excel file. 
    You can download the template in the sidebar and re-upload it with your data.
    \n In order to understand the parameters, a small description can be found below. 
    Together with the discription of the formulas.
    ''')

def analytical_TT():
    

    st.write('''
    #### Top tensile test
    The deformation process during a top tensile test can be compared with that of the **tube sinking process without a mandrel**. This implies 
    that the die-side sheet can be seen as a rigid ‘die’. The most basic formula applies when the clinch is simplified to a tube. Because of 
    oversimplification, the maximum force will be underestimated. According to Coppieters et al. [[1]](https://www.sciencedirect.com/science/article/pii/S0263823111002679?casa_token=B9vJYddxRZwAAAAA:5qLzJcUV4gLqi2gJPE3CC38byUndCJ8UfmIoVFduI26Dy3b0XCoLJw55gXLHm4FdiM2AsEBYMekKXg), 
    the bottom part of the clinch contributes to the strength as it is radially compressed when assuming a rigid die (original). If the edges of the shape are more strictly delineated, 
    by means of the typical geometric parameters, an even better prediction of the force is obtained.
    > *The maximum top tensile force of **deformation-dominant failure** is calculated according to Coppieters (see below). But with different boundary conditions.*
    ''')

    
    
    render_latex(r"F_{def} = {A_n\left[-\frac{4\pi}{\sqrt{3}}\sigma_{yield}^{Tube}\left(\frac{1+\beta}{\omega}\right)+\left(\frac{A^{Rod}_{exit}\sigma^{Rod}_{yield}\left(\frac{1+\beta}{\beta}\right)\left[1-\left(\frac{A^{Rod}_{exit}}{A^{Rod}_{entry}}\right)^{\beta}\right]}{A^{Tube}_{entry}}+\frac{4\pi}{\sqrt{3}}\sigma_{yield}^{Tube}\left(\frac{1+\beta}{\omega}\right)\right)\left(\frac{A^{Tube}_{entry}}{A_n}\right)^{\frac{\omega}{2\pi}}\right]}")

    # render_latex(r"F_{def} = {A_{n,tube}\left[\frac{2}{\sqrt{3}}\sigma_{yield}^{Tube}\left(\frac{1+\beta}{\beta}\right)+\left(\frac{A^{Rod}_{exit}\sigma^{Rod}_{yield}\left(\frac{1+\beta}{\beta}\right)\left[1-\left(\frac{A^{Rod}_{exit}}{A_f}\right)^{\beta}\right]}{A^{Tube}_{entry}}-\frac{2}{\sqrt{3}}\sigma_{yield}^{Tube}\left(\frac{1+\beta}{\beta}\right)\right)\left(\frac{A_{n,tube}}{A^{Tube}_{entry}}\right)^{\beta}\right]}")
    st.write('''
    The top sheet is the thinnest in the neck region meaning that the joint will fracture in this region. This failure mode can be compared to an 
    uniaxial tensile test on a tubular specimen with a thickness equal to the neck thickness [[2]](https://www.sciencedirect.com/science/article/pii/S0261306909006220). This calculation is fully analytical when the area is derived from experimental data.
    > *The **fracture strength** can be calculated as follows:*
    ''')
    render_latex(r'''F_{frac} = A_n\sigma_{UTS}''')
    
def analytical_ST():
    st.write('''
    #### Shear lap tensile test
    When applying a shear load on two clinched sheets, a complex deformation of the joint and sheets will occur. The most simplified 
    representation is a tube under shear loading. Due to the large deformation and associated strain hardening of the sheets during clinching, the local yield stress has increased.
    Therefore, numerical data is needed to determine the yield stress after joining (AFS)''')
    render_latex(r'''F_{def} = A_n\frac{\sigma_{AFS}}{\sqrt{3}}''')
    st.write('''
    An empirical method was used to calculate the strength until fracture. 
    ''')
    render_latex(r'''F_{frac} = \frac{t_1\alpha}{4}(2d+\alpha t_1)\pi\sigma_{UTS} \quad with: \quad \alpha=0.4''')
    
def results(strengthTT,modeTT,strengthST,modeST):
    st.write(f'''
    Based on the manual input, we expect the joint to fail around **{strengthTT} during a top tensile test**. Where {modeTT} failure is dominant. 
    During **a shear lap test**, we predict that the joint can withstand **{strengthST}** with {modeST} as dominant failure mode.
    \n The results of all 4 calculations can be seen in the table below: 
    ''')

def  Machine_General():
    st.write('''
    ### General
     
    ''')

    centerImage(pathImage='docs/ML1.jpg',width='65%',
            underscript='')

def WF_experiments():
    st.write('''
    ### General
    The first step towards the strength prognosis of a clinch joint is collecting experimental data. 
    This data is then used for the validation of finite element (FE) simulations as well as for the prognosis quality 
    of data-based algorithm. Based on four materials (three steel and one aluminium grade) with minimum three 
    different sheet thicknesses, a statistical test plan with 73 material combinations was created for the experimental tests.
    \n
    ### Experimental data of the joint
    \n In order to validate the stress state within the material, the force-displacement curve was measured during 
    the joining process. To take this into account during machine learning, the maximum setting force was used as an input value.
    ''')

    centerImage(pathImage='docs/ProcessCurve.jpg',width='40%',
            underscript='')

    st.write('''
    The typical geometrical parameters were also measured via a cross section analysis. These parameters were used for 
    the validation and as input values for the machine learning. The cross section itself was used to tune the friction 
    parameters so the joint contour from the simulation  would be identical to the experiment.
    ''')
    
    centerImage(pathImage='docs/CrossSection-M.png',width='60%',
            underscript='')

    st.write('''
    ### Experimental data of the joint strength
    \n For the strength, two different loading conditions were tested, pull-out or top tensile test and the shear lap test. 
    From the process curves, only the maximum force (joint strength) was used in further steps.
    ''')
    centerImage(pathImage='docs/StrengthTests.jpg',width='80%',
            underscript='Two loading conditions used for the determination of the max force. Left: Pull-out Right: Shear lap')

def WF_simulations():
    st.write('''
    ### General
    For the strength prediction with the help of data-based algorithms, a large database needs to be created. 
    This is possible with only experimental data, but this would be resource and labor intensive. Therefore, in the second step, 
    we replicate the experiments using an FE-software named [Simufact forming](https://www.simufact.com/simufactforming-forming-simulation.html). 
    We try to minimize the computational time while maintaining  an acceptable deviation over all three simulation 
    steps. Through existing functions in this software, it was possible to automate the results transfer from the 
    joining simulation to the strength test. Which decreased the conversion time drastically.
    ### Simulation
    Before we can calculate the strength of the joint with FE-software, the material must be characterized 
    and a friction model must be selected. For the flow curve of the material showed the stack compression 
    method the best results. The combine friction method is used due to the fact that it had more influence 
    on the contour. The parameters was tuned for all 73 cases individually.
    ''')

    centerImage(pathImage='docs/Simulation-Strategy.jpg',width='70%',
            underscript='Deviation between the numerical and experimental data of the 50 best simulations')

    st.write('''
    For the simulation of the joining process (see below) and the pull-out test, a axisymmetric (2D) 
    model was used to reduce computational time. The results of the joining process was automatically 
    imported into the strength simulation and revolved for the shear lap test because this was a 3D simulation.
    ### Results
    For each simulation step, a deviation between the experiment was calculated. Based on the 
    average of those steps, 50 out of 73 cases were selected for the next step. This is to improve 
    our accuracy of the virtual database.
    ''')

    centerImage(pathImage='docs/ResultsSimulation.jpg',width='70%',
            underscript='Deviation between the numerical and experimental data of the 50 best simulations')

def WF_DoE():
    st.write('''
    ### General
    From the 73 experiments, we selected the 50 best simulations. With those databases is it possible 
    to train some basic machine learning algorithms. But, once you use more advanced models, there 
    is a need for more data. To achieve a larger database, variations are made on the 50 best validated 
    simulations. With the help of these virtual experiments, we can lower the cost and save resources. 
    By making several parameters variable, you rapidly end up with a large amount of variations. 
    Therefore we do a Design of Experiments (DoE) to select 20 variations without losing the overall 
    responds of all possible combinations. In the function tab above, you can create your own DoE. 
    Because we are working in a virtual environment, variations on the tools are cheaper to accomplice.   
    ''')

    centerImage(pathImage='docs/Principle_DoE.jpg',width='70%',
            underscript='')

    st.write('''
    ### Variable parameters
    The parameters are chosen based on there influence on the geometrical parameters and strength of the joint. 	
    > * Material property: Scaling flow curve
    > * Process parameter: Bottom thickness tb
    > * Tool geometry:
    ''')
    centerImage(pathImage='docs/VariedParameters.jpg',width='50%',
            underscript='')

def WF_MachineLearning():
    st.write('''
    Genaral
    ''')

def WF_function_DoE():
    st.write('''
    ### How it works
    With this function is it possible to do your own design of experiment. With the help of the 
    Latin hypercube sampling method,  a certain amount of samples can be taken from the 
    larger matrix with all possible combinations. To do the DoE, the following steps need to be undertaken:
    >   1.	Fill in the names of the parameters you want to vary. There must be at least two variables filled in.
    >   2.	Open the sidebar by pressing on **'>'** in the top left corner. 
    >   3.	Select the amount of samples you want to take.
    >   4.	Define each parameters: discreet or continue and the boundaries.
    >   5.	Download the DoE under the visualization of the first 2 variables

    ''')

def WF_function_ML_Train():
    emptycol1,col,emptycol2=st.columns([1,6,1])
    st.write('''
    ### How it works
    This function makes it possible to train six different regression algorithms. Before using 
    this function, we recommend you to read the machine learning tab first. This will give you 
    more insight of the working and workflow of machine learning. With this function is it 
    possible to train and save your best model for each algorithm and output variable. This 
    is possible after completing the following steps:
    ''')
    with st.expander("1.    Define the database:"):
        st.write('''
        -Standard, the database of the project is used. There is also the possibility to upload your 
        own database. Simply upload your file and select uploaded in the drop down menu.
        ''')
    
    with st.expander("2.	Define the in- and output:"):
        st.write('''
        Start with selecting the output variables that you want to predict. By pressing on the 
        button **‘Transfer remaining variables to input’**, all remaining names transfer to the 
        drop down menu on the right. Delete the variables you don’t need. Once you press on 
        **‘Set the in- & output’**, a visualization of the database is created with the colors for the in- 
        and output. Press **‘Yes’** to continue with these settings.
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
        To improve the prediction possibility of the algorithm, it is possible tune the 
        hyperparameters. If you hover over the **‘?’**, a short description is given for that 
        hyperparameter. Select the ones you want to change and press on **‘Start tuning …’**
        ''')
    
    with st.expander("5.	Define the boundaries of the hyperparameters:"):
        st.write('''
        With the use of a grid search, all possible combinations of hyperparameters will be tried out. 
        Consequently, training time will increase drastically when you increase the possible 
        values of the hyperparameters.  Based on the type of the hyperparameter, different boundaries 
        will be defined. For a integer of float, a min and max boundary needs to be defined. As wall 
        as an value **‘#’** what divides the interval in that amount of equal parts. The bigger this 
        value, the more time it will take to train the model. Press **‘Start to train’** when all 
        boundaries are defined.
        ''')
    
    with st.expander("6.	Train the model:"):
        st.write('''
        Because the algorithm can only be trained for one specific output variable at once, 
        this needs to be selected. Now, press on **‘Train’** and wait until a table and graph is 
        plotted. In the table can all possible combinations be found with their r²-value. In 
        the most right column, you can rearrange the table based on their rank. This can help 
        to tune the hyperparameters even more. In the graph, the prediction against the 
        measured value can be seen for the best (ranked as number 1) hyper settings. Once 
        you are satisfied with the result, press on **‘Download the trained model’**. This will 
        download the best model that you have achieved for that particular algorithm, 
        hyperparameters and output variable. With this file is it know possible to go to 
        the function ML-Predicting.
        ''')

    st.write('''
    ### Start training
    ''')

def WF_function_ML_Predict():
    st.write('''
    ### How it works
    Before you can do your prediction, a machine learning model needs to be trained. This 
    can be done in the function tab ML-training. Once you have this, upload this file below 
    this text. Now, two options can  be selected in the sidebar:
    >   1.	**Manual:** Based on the input variables of the model, input field are created in the sidebar. With this method, a fast prediction can be made for one case.
    >   2.	**Excel:** Based on the input variables of the model, a template (csv file) with the correct column tags can be downloaded. Complete this with your data and save this an excel file. After you re-upload this file, the predictions can be downloaded.
    ### Start predicting
    ''')