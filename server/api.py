# -*- coding: utf-8 -*-

from flask import Blueprint, current_app, jsonify, request
from search import *


api = Blueprint('api', __name__)

	
def data_path(filename):
	data_path = current_app.config['DATA_PATH']
	return u"%s/%s" % (data_path, filename)


@api.route('/search', methods=['GET'])
def search():

	# Specify default values for later input validation.
	radius = request.args.get('radius', -1.0, type=float)
	count  = request.args.get('count', -1, type=int)
	tags   = request.args.get('tags', '', type=str)
	lat    = request.args.get('lat', -999.0, type=float)
	lng    = request.args.get('lng', -999.0, type=float)

	if radius < 0 or count < 0:		# this can happen when using dropdowns
		return ('bad parameters', 400)
		
	if lng > 180.0 or lng < -180.0 or lat > 90.0 or lat < -90.0:	# no idea how you got there
		return ('bad position', 400)

	shops_df = pd.read_csv(data_path('shops.csv'))

	if tags != '':
		tags_df = pd.read_csv(data_path('tags.csv'))
		tag_ids = get_tag_ids_by_tags(tags_df, tags.split(','))

		if len(tag_ids) > 0:
			taggings_df = pd.read_csv(data_path('taggings.csv'))
			shops_df = filter_shops_by_tag_ids(shops_df, taggings_df, tag_ids)
			if shops_df.shape[0] == 0:
				return ('No shops with tag(s).', 404)

		else:
			return ('No shops with tag(s)', 400)

	shops_df = filter_shops_by_location(shops_df, (lat, lng), radius)
	if shops_df.shape[0] == 0:
		return ('No shops found.', 404)

	shop_ids = shops_df['id'].tolist()
	products_df = pd.read_csv(data_path('products.csv'))
	filtered_products_df = filter_products_by_shop_ids(products_df, shop_ids)
	if filtered_products_df.shape[0] == 0:
		return ('No products.', 404)

	final_products_df = finalize_products(filtered_products_df, count)
	products = products_to_dicts(final_products_df, shops_df)
		
	response = jsonify(products)
	return response













