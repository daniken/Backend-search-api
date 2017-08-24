### **Files of interest**
API search methods can be found in `server/search.py`. 
Tests can be found in `test/tests.py`.

Executing `python tests.py` in the test folder will clock some operations while executing `pytest tests.py` will perform assertion tests.

### **Additional dependencies**
`pandas` for handling and manipulating csv files.

### **Backend logic**
* Error-check input parameters
* If tags are provided:
    * Find corresponding ID of existing tags
    * Filter shops by tag IDs
* Filter shops by location
* Filter products by shop
* Sort products
* Remove out-of-stock products and limit the number of products to return

---------

### **Correctness**
* The backend returns a list of the most popular products of all the shops within the given radius which seems to be the intended output of this endpoint. But while constructing the pins for each product, multiple products may be originate from the same shop, which will result in multiple pins at the same exact shop location. This is a problem since, while hovering over the pins, only one product pin of the same shop can be displayed at a time. This is not well thought out...

### **Quality & Design**
* I take for granted that column-labels in the provided .csv files are finalized. In a production setting, my code would break if the column-names would be renamed.
* I would consider writing more (and better) tests for the functions I wrote and ensure they return what I imagine they intend to return. I kind of did this during implementation using jupyter notebook as a fast way check code snippets, but I did not document all of it.
* I would consider clock more of my operations against other possible operations that produce the same results and analyze their performance in different settings.
* I have not considered handling multiple clients. I've tried the API using two browser tabs simultaneously but I don't know exactly how this affects the server load.
* I have not considered any memory management which is a important aspect to consider.
* Give more informative error messages in what went wrong when an error is  raised.

### **Performance**
* While searching for tag IDs that match any of the specified tags, a small performance improvement would be to remove a tag, once found, from the list in which we are matching against. This would reduce the number of comparisons. This improvement is rather small since the number of tags are miniscule compared to, for example, the number of products. 
* Preprocess the specified tags and remove bad ones e.g. 'sh1rts', 'lamp(s)' etc. before finding tag IDs of valid tags.
* The performance could be sped up if we had a data structure holding product IDs for every shop. Possibly a column in shops.csv with all product IDs of that shop seperated by a comma or using a hash table/dictionary structure. Then we wouldn't have to load and go through ALL products while matching against shop IDs of just a few products. The same goes for tags for each shop.
* Performance tests show that it is currently faster to first filter shops by tags (if provided) then filter by location instead of first filtering by location and then by tags. This may change depending on the relative sizes of the involved datasets.
* One could consider clustering the shops by regions to reduce the amount of shops to consider while filtering by location which improves the performance.













