import pandas as pd
import math

### methods supporting search API ###

EARTH_RADIUS = 6371e3 # earth's mean radius


#	Uses Haversine formula to calculate the distance between two geo-positions.
#	Returns True if distance between @u and @v=(v0,v1) is less or equal to @r
# 	@param {Series}		u	Represents a shop.
# 	@param {Float}		v0	Client's latitude coordinate.
# 	@param {Float}		v1	Client's longitude coordinate.
# 	@param {Float}		r	Maxmimum distance between @u and @v.
def compute_if_within(u, v0, v1, r):
	lat1 = math.radians(u['lat']) 	
	lng1 = math.radians(u['lng'])

	lat2 = math.radians(v0)
	lng2 = math.radians(v1)

	delta_lat = lat2 - lat1
	delta_lng = lng2 - lng1

	a = math.sin(delta_lat/2.0)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lng / 2.0)**2
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
	return EARTH_RADIUS * c <= r


#	Returns a list of tag IDs that matched against client's tags.
#	@param {Dataframe}	tags_df 	Dataframe with structure as tags.csv.
#	@param {list} 		client_tags 	Contains specified tags that we want to match against.
def get_tag_ids_by_tags(tags_df, client_tags):
	return [tags_df.loc[i, 'id'] for i in range(tags_df.shape[0]) if tags_df.loc[i, 'tag'] in client_tags]


#	Returns a filtered pandas dataframe with shops that are within the radius of client's geo-position.
#	@param {Dataframe}	shops_df	Dataframe with structure as shops.csv to be filtered.
#	@param {Tuple} 		client_pos 	Contains lat. and lng. coordinates of client's current geo-position.
# 	@param {Float}		radius		Specified search radius in units of meters.
def filter_shops_by_location(shops_df, client_pos, radius):
	return shops_df[shops_df.apply(compute_if_within, axis=1, args=(client_pos[0], client_pos[1], radius,))]


#	Returns a filtered pandas dataframe with shops that have atleast one matching tag in @tag_ids.
#	@param {Dataframe}	shops_df 	Dataframe with structure as shops.csv to be filtered.
#	@param {Dataframe}	taggings_df 	Dataframe with structure as taggings.csv for relating shops with tags.
#	@param {list}		tag_ids 	Contains tag IDs for the tags we want to match against.
def filter_shops_by_tag_ids(shops_df, taggings_df, tag_ids):

	shop_ids_by_tags = set(taggings_df[taggings_df['tag_id'].isin(tag_ids)]['shop_id'].tolist())
	return  shops_df[shops_df['id'].isin(shop_ids_by_tags)]


# 	Returns a filtered pandas dataframe with products from the shops in @shop_ids.
#	@param {Dataframe} products_df 	Dataframe with structure as products.csv to be filtered.
#	@param {list} shops_ids 	Contains shop IDs for the shops we want to match against.
def filter_products_by_shop_ids(products_df, shop_ids):
	return products_df[products_df['shop_id'].isin(shop_ids)]


#	Sorts rows in @products_df w.r.t. popularity.
#	Removes out-of-stock products and returns a dataframe with a maximum length of @count.
#	@param {Dataframe}	products_df 	Dataframe with structure as products.csv.
#	@param {Integer} 	count 		Maxmimum number of products to display.
def finalize_products(products_df, count):

	temp_df = products_df.sort_values('popularity', axis=0, ascending=False)

	product_indices = []
	n_products = 0

	# breaks once @count products in-stock has been found
	for idx in range(temp_df.shape[0]):
		
		if temp_df.iloc[idx,:]['quantity'] != 0:
			product_indices.append(idx)
			n_products += 1
			if n_products > count:
				break

	return temp_df.iloc[product_indices,:]


#	Returns a list of dictionaries, each dictionary corresponding to a product.
#	Each dictionary has information such as product title, popularity and nested shop coordinates
#	@param {Dataframe} products_df	Dataframe with structure as products.csv containing the final products.
#	@param {Dataframe} shops_df 	Dataframe with structure as shops.csv for relating geo-positions to products.
def products_to_dicts(products_df, shops_df):
	
	# Need column-indices of 'lat' and 'lng' to access values via .iloc[].
	lat_idx = shops_df.columns.get_loc('lat')
	lng_idx = shops_df.columns.get_loc('lng')

	products = []
	for idx in products_df.index.values:

		shop_id = products_df.loc[idx, 'shop_id']

		lat = shops_df.loc[shops_df['id'] == shop_id].iloc[0,lat_idx]
		lng = shops_df.loc[shops_df['id'] == shop_id].iloc[0,lng_idx]
		title = products_df.loc[idx, 'title']
		popularity = products_df.loc[idx, 'popularity']
		shop = {'lat':lat, 'lng':lng}

		products.append({'shop': shop, 'popularity':popularity, 'title':title})

	return products

