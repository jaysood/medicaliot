In order to run the software, the following dependencies are required:
scikit-learn
matplotlib
NumPy
Pandas

Furthermore, Python 3.7+ is required.
Recommended to be run in a virtual environment such as virtualenv, env etc.

NOTE: In the file convert.py YOU MUST CHANGE the path for "generatedDataFile" and "iomtDataFile"
to wherever the software is located on your machine. THE SOFTWARE WILL NOT WORK OTHERWISE.

If you are getting issues with matplotlib, try changing the backend! Note, this is set to 'macosx' in:
knn.py
naivebayes.py
randomforest.py
svm.py

Try changing it to tkAgg or similar. See: https://matplotlib.org/faq/usage_faq.html#what-is-a-backend for more details.




Running Instructions:

Run datagen.py FIRST.
Enter whether you want training or test data generated.
Enter the amount of data you wish to generate. (Note takes a while for 100,000+ entries!)

Run one of the mlmethods. Experiment!


- Jay Rauniar Sood, 2019/2020 -
