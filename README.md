# Book-Recommendation-Systems
Στο παρόν προτζεκ αντλούμε δεδομένα από μια βάση δεδομένων από το [Book-Crossing Dataset](http://www2.informatik.uni-freiburg.de/~cziegler/BX/BX-CSV-Dump.zip), η οποία αναφέρεται σε χρήστες, βιβλία και βαθμολογίες που έχουν κάνει η χρήστες σε αυτά. Το πρόγραμμα επιλεγεί τυχαία 5 χρήστες και παράγει  τα προτεινόμενα βιβλία με βάση το προφίλ τους. Δηλαδή παράγει 2 αρχεία για κάθε χρήστη με 10 βιβλία το καθένα, μια με βάση την ομοιότητα Jaccard και μια με βάση  την ομοιότητα Dice coefficient. Για να τρέξει το πρόγραμμα απαραίτητο είναι να υπάρχουν τα αρχεια csv από το παραπάνω σύνδεσμο στον ιδιο φάκελο με το προτζεκτ.

# In the project directory, you can run:

## Available Libraries
<br/>
Import NLTK library

### `pip install nltk`

## Run 

First run the Clean_data_and_Generate_Keywords.py 
### `python Clean_data_and_Generate_Keywords.py`



After run the Recommended_system.py 
### `python Recommended_system.py`
