# -*- coding: utf-8 -*-

import pandas as pd
import pytest
import time
import os
import sys

# Set up the path to import from `server`.
root = os.path.join(os.path.dirname(__file__))
package = os.path.join(root, '..')
sys.path.insert(0, os.path.abspath(package))

from server.search import *

# predefined client geo-position
client_lat, client_lng = 59.3325800, 18.0649000	
client_pos = (client_lat, client_lng)			

# predefined search radius
radius = 500

# number of iterations when clocking functions							
iterations = 5

# earth's mean radius									
R = 6371e3 										

# predefined shop IDs to match against in the tests below
shop_ids = [
'168fe6a5d7974cef8a77c7cc7e1cfb9d',
'860230bfd7124e0e9a3fab948ec845c2',
'4b2070d803944c48880c057ef27f79e3',
'b3cfc6c2ee824e1e9fe4cf33bf3f7005',
'9ca604dec5604dfb93932723db2c948c',
'8b33e5ceb25e4b9b9829abeec1d7be65',
'4c5d56c1b2e94e3bac25c700cda66c41',
'83e630c7394747778f0a03f6dc8103e4',
'0ae9ebdd7fec4976ba929f0385ff841e',
'c45b130576fb4cc58e9357b8bfd518e6',
'4b03231442924d0eb48fc81ad59e7172',
'7e8868b468fa408c9b855c1c66ac0591',
'68527f72cb4b4835b72b5472f1667146',
'974b8dc7281f419abbaf7653af0a7cb6',
'c198b8c9a3374f2ea68f2cc492f37ebf',
'b1703c1a7f2a49d3bf831b1b3be51193',
'35b01da104f242e5a70ca50dc7f3499b',
'427e66462bef4dd5ac0766a4f5b29f6f',
'1ad4e2a78f244c7e824578e1741c2e5b',
'248e4f23d500429f943942b42705c6b1',
'979dc2c77160448c8a9f70b3dae158f7',
'0163ba4834df4feaa4f6f5e3600d6ba5',
'ce4a89972a66490b83d91ffd82f13710',
'70dd7b69a5464484bd8bb0f96a0a32d3',
'be4fd6c2bfb54db39d36c81e2af0140a',
'edf7205bcbd1479ebf6fbc15cf6e0f47',
'db5cc1702a8247bdb1dd7982d17c0079',
'3a852998a6be48c4899842ca83f25d05',
'3692be665b104167916e81e8708215cf',
'f180d37918be47648c239ba72acf3c78',
'b06da62ca8734ee6b10cce548facff42',
'a1c18c4b63cb4136b4b8dbd827030dce',
'b804e80b6781410292f045f89f684dd6',
'35f3e7cb10824b65af9120bb0c9a39c6',
'9bcdedafcec7452784600d08cbf6b55d',
'30a5a457198d4c5993860929768908e8',
'5c90fb2d83854392b1df369a87353559',
'beb7b00010f84ada8e1391590d1a761c',
'ae36533bb5f6478e91f14aa17e65443c',
'e04be2fedc024f09817a494425a4a5ee',
'985b7e5a266841a09d21147dc320e8d4',
'9bb0b4d60c8f48fa823cd42b35e2f7e5',
'87c65867dac1499296b44de482e3af11',
'2655b64341f14d96bf57301de7f7b205',
'79629fd1c1144e84a5b757207d8589b2',
'55aab3f217d64e598ab3a423479e2dfd',
'7bc78f96424349e194580f2464a64cbb',
'db14200895d741cb8507854bdb897c48',
'6e7a4209a7d74a2d8a12f5c9ed7c85ee',
'cf9a766228224d1bb33ce1074ff7c981',
'41696d3f31ea4789a4dfe2e38ae0af25',
'6bd93c122e494e9c8898b862a2e01103',
'b3a58587abf442cbab0662340c687690',
'e79adec284664c45a735e17de1e82735',
'47791f17b876415090a885631a6a9556',
'c2a19ba1727846eb909c510d682d2906',
'635d4699383e4f348c2b6e96d19bfaf8',
'6a0f44f1445a4e2d8c4bebb15771e99b',
'251551b77d1c4bd497e95829e14f172c',
'88e054518a8346afa4efca64c80644e8',
'8a7122ff1a7d4da7809f45fa35e5b977',
'9109fa44713e449ab20d6ca52d230252',
'3ceb123aa6d7412d844ab627616138dd',
'cbf6aa2edc4d488386d8a6789e449e51',
'df5ecd91482d455eb320242b2462f890',
'3650ab935edd4a9abfc204af506eda3b',
'f9c2df6330554bd28bb4617a847e6e01',
'3ace0dea68cd4df4a43063faa1c2944c',
'488cd65a2eef419cb15e11aec3142f50',
'7b3499e5f77c491c821499351918dc88',
'a6f2ac8e099145bc804c355a168bddfd',
'b4ddd5b915cd4fec8bd15b7dffbc23ee',
'a4313b0c3b8b4facb8430b6f38028070',
'62fdfee1148048a88d39a34058148005',
'6a2c37de29894537a7d031f286704662',
'a169d3e508724aa19f4bab33e5261329',
'44cfe05fd49b4fecbb1b9824fa043131',
'54afed062c3c4ac68553f11d7cca27aa',
'a1a8ddcbb9a743a2af58404a84a7c667',
'148561ea2941432da869b2213c154e78',
'6c18fd9303864b24aa37e308b5409263',
'322f59c22fda4ad5b9d26656cd5a80e4',
'd4f6e5e5e1d94fe8aadce06ec3c3fa88',
'1bf62d82b0b14cf89dac2e5d153fb3aa',
'97867c4b078442d7b751df7d4c4ac595',
'06eea02cfa7449d89e4cb14bd500dbd4',
'184dcf9ca1e8461e91e69764c3dafac7',
'd3d67409a3de486fb361b2f0f35f8c10',
'9b52813b3bd64c30803ad5d6aa992908',
'fdd9790c2a8e4608a50b30303f61911c',
'f1cf50549fd94594ba61340f0dc32e23',
'c06c3ea28be24d90b2c0d993afa38ee9',
'ee403757b14246a6be89550db167c478',
'1ecfce7163154fbca89d5c8ae001988c',
'cff703e58de14bab84316bda924711d4',
'2931124e9f444f6e9fc9bebd4552bd03',
'3599f04967624925bfaab3d8984a792f',
'6114aa5512b94e688446b5f17da5ae61',
'556289bff8b842a4bc6db6169a7030a2',
'1c446c481ac240a2adaec6505506393e',
'8011e71eb0344eca80eec0ac101e293a',
'8e8ec3b2d08d4439a1a9fe719e11d9f6',
'ecec023563a04debbd7cbc785a8b35f0',
'0ecbeed6421b472b87c887d84a1743da',
'4e4928e2c0134821816bf51cfd58d1b3',
'af82a515082048b1b912e6f14e9f029b',
'4408561f9cab42178c4a693e626e4c7f',
'87fd316133c046c393981f04f01a72f2',
'aff3ed3fbc494ba38bdeb8f7b95e20ce',
'c49d8e6c17e441d4aa9e31b676789dea',
'a632dccbab43488da48253d713d12052',
'0ba653c8921941e9b483101f6118b8c7',
'dfb7c7b05e6349da8472b6cb45888d63',
'116763addfba4933a1c7154ef769e369',
'7c9d8cf5778d44d5ac85bc2a3de43048',
'18ac4e1636444b45ad0f704294db5de2',
'3dc819f05e5d41338fde6617faf0dcff',
'85da1e19caa94c00b2160d8db45e9719',
'fe917143d8564ad7954a3cab03805597',
'63c0a8902cdb4baabf14b505b936b6e0',
'6aefb580ea6449f09f03d83820e8cde5',
'4db86c3ab74c443ba8036644b7f18eeb',
'0f1e5b47c3e44563bbc10bccab73b841',
'f2880a3cb3c944329cfba5b3d0ee2ef7',
'428a86ebc04c47dcb2c5bebdda328ecb',
'4daa99fcbe2341db9216209dc4592a83',
'04ef0913496e482f9bd9071eeefb1464',
'7aecb9e9f3dc4a9a92e2c86ceeea459c',
'88860b00f7da4cfbbc7d76597ba58da7',
'9f5508c352c149aa9b5df751759576c7',
'f470188d609144e3839e556d7bea96bb',
'13e85b7663f34293b21ae0343d2cc661',
'2b31f44cd42c41adb1b7a93499982ee3',
'ab1269c313924e9da4a092b0c2dff810',
'8e3e698c66744122983715bfcd9489d8',
'd5982c42e3df419cb7c3266159435167',
'caf6b468db1841aa864fb742690da0b6',
'37e282afb6d84ea98eb459878f0f2107',
'e207ac35f413499bb301f42e5a896248',
'5ea329e535d14d48b561882fc9383a8a',
'7db11076ab4d47de8cb82a7dad9a9a8a',
'4bd48ebadc884063bab8f0f2f8c44ecf',
'c92abebb3c5541cd81b7c86fb5ddd5fe',
'f1fbe85037124629aed9ee5834fdb268',
'd67c2971b08947bebb643c86276d35c3',
'b98a2968c2ab4b14b808005b22b70d24',
'df5bdbb31adc48b1b2dad5e6cc06ff0a',
'eb745dfeb96a43eab9e76ae2a14c48eb',
'7b7ab2b1d6a74bcb9c6469bb6ba82d37',
'ee371e70b18441f28ab72ebb3f37b31c',
'131fab1599c24b1ab62382269ed57556',
'988ac46c2430420d92c3a69c49c42970',
'0be2b29b481f4f2da53870dc1fb914a0',
'c2793b785b2d44cfbb43c1b1ce771e5d',
'889d4acfd763446eadcca044a8c08b57',
'42bb38e8395d41569d9d2b9540b60eab']
 
# predefined tag IDs to match against in the tests below
tag_ids = [
'f92c55a2cbc84439babb003062282f92',
'6c9030185c074b62aa5d5c702ce2dca0',
'4a6cf7ee90f74f12869e8bdbc90398b9']

# predefined tag to match against in the tests below
client_tags = [
'kids',
'cool',
'shirts',
'dog',
'university',
'tops',
'formal',
'fashion']


#	Uses parts of Haversine formula to calculate the latitude distance between two geo-positions.
#	Returns True if latitude distance between @u and @v=(v0,v1) is less or equal to @r
def is_within_lat(u, v0, r):

	lat1 = math.radians(u['lat'])
	lat2 = math.radians(v0)

	delta_lat = lat2 - lat1

	a = math.sin(delta_lat/2.0)**2
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
	return R * c <= r


###
### Functions that filters shops by location ###
###	

#	uses .apply() filter out shops by location
def filter_shops_by_location_one():
	
	shops_df = pd.read_csv('../data/shops.csv') 
	return shops_df[shops_df.apply(compute_if_within, axis=1, args=(client_lat, client_lng, radius,))]

#	Finds indices of shops that are within the radius using a wrapped-for-loop
def filter_shops_by_location_two():

	shops_df = pd.read_csv('../data/shops.csv') 

	id_idx = shops_df.columns.get_loc('id')
	lat_idx = shops_df.columns.get_loc('lat')
	lng_idx = shops_df.columns.get_loc('lng')

	indices =  [i for i in range(shops_df.shape[0]) if compute_if_within(shops_df.iloc[i], client_lat, client_lng, radius)]

	return shops_df.iloc[indices]


#	First computes if latitude coordinates are within the bounds then same as function_one
def filter_shops_by_location_three():

	shops_df = pd.read_csv('../data/shops.csv')
	shops_df = shops_df[shops_df.apply(is_within_lat, axis=1, args=(client_lat, radius,))]

	return shops_df[shops_df.apply(compute_if_within, axis=1, args=(client_lat, client_lng, radius,))]







###
### Functions that filters shops by shop IDs ###
###

def filter_shops_by_id_one():
	shops_df = pd.read_csv('../data/shops.csv')
	return shops_df[shops_df['id'].isin(shop_ids)]


def filter_shops_by_id_two():
	shops_df = pd.read_csv('../data/shops.csv')
	return shops_df.set_index(shops_df.loc[:,'id']).loc[shop_ids]
	#shops.index = pd.RangeIndex(shops.shape[0])





###
### Functions that filter shops by tag IDs and location in different orders/ways ###
###

#	First filters by location and then
#	checks for tags using for-loop over all located shops
def filter_shops_by_tag_ids_one():

	shops_df = filter_shops_by_location_one()

	taggings_df = pd.read_csv('../data/taggings.csv')
	taggings_idf = taggings_df.set_index(taggings_df['shop_id'])

	shop_indicies_with_tag = []
	i = 0
	for shop_id in shops_df['id']:

		shop_tag_ids = taggings_idf.loc[shop_id]['tag_id'].tolist()

		for tag_id in tag_ids:
			if tag_id in shop_tag_ids:
				shop_indicies_with_tag.append(i)
				break	# Found one match, no need to continue searching.

		i += 1
	return shops_df.iloc[shop_indicies_with_tag, :]


#	First filters taggings by tag IDs using a baked-for-loop then
#	filters by location.
def filter_shops_by_tag_ids_two():

	# find shop IDs with matching tag IDs
	taggings_df = pd.read_csv('../data/taggings.csv')
	shop_ids = set([taggings_df.loc[i,'shop_id'] for i in range(taggings_df.shape[0]) if taggings_df.loc[i, 'tag_id'] in tag_ids])

	shops_df = pd.read_csv('../data/shops.csv')
	shops_df = shops_df[shops_df['id'].isin(shop_ids)]

	return filter_shops_by_location(shops_df, client_pos, radius)


#	First filters taggings by tag IDs using .isin() then
#	filters shops by location
def filter_shops_by_tag_ids_three():

	taggings_df = pd.read_csv('../data/taggings.csv')
	shop_ids = set(taggings_df[taggings_df['tag_id'].isin(tag_ids)]['shop_id'].tolist())

	shops_df = pd.read_csv('../data/shops.csv')
	shops_df = shops_df[shops_df['id'].isin(shop_ids)]

	return filter_shops_by_location(shops_df, client_pos, radius)


#	First filters shops by location then
#	filters taggings_df by located shop IDs then
#	filters by tag IDs.
def filter_shops_by_tag_ids_four():
		
	shops_df = filter_shops_by_location_one()
	shop_ids = shops_df['id'].tolist()
	
	taggings_df = pd.read_csv('../data/taggings.csv')
	taggings_df = taggings_df[taggings_df['shop_id'].isin(shop_ids)]
	
	shop_ids = set(taggings_df[taggings_df['tag_id'].isin(tag_ids)]['shop_id'].tolist())

	return shops_df[shops_df['id'].isin(shop_ids)]
	

#	First filters shops by location then filters taggings_df by tag IDs then
#	finds the intersecting shops IDs
def filter_shops_by_tag_ids_five():
		
	shops_df = filter_shops_by_location_one()
	shop_ids_by_location = shops_df['id'].tolist()
	
	taggings_df = pd.read_csv('../data/taggings.csv')
	shop_ids_by_tags = taggings_df[taggings_df['tag_id'].isin(tag_ids)]['shop_id'].tolist()
	
	shop_ids = set(shop_ids_by_location).intersection(set(shop_ids_by_tags))
	return shops_df[shops_df['id'].isin(shop_ids)]
	







###
### Functions that filters tag IDs by tags ###
###

def filter_tag_ids_by_tags_one():
	tags_df = pd.read_csv('../data/tags.csv')
	return [tags_df.loc[i, 'id'] for i in range(tags_df.shape[0]) if tags_df.loc[i, 'tag'] in client_tags]


def filter_tag_ids_by_tags_two():
	tags_df = pd.read_csv('../data/tags.csv')
	return tags_df[tags_df['tag'].isin(client_tags)]['id'].tolist()







###
###	Test class that verifies that all IDs is shops.csv, tags.csv and products.csv are unique ###
###
class TestCSVData(object):
	
	def test_shops(self):
		shops_df = pd.read_csv('../data/shops.csv')
		assert shops_df.shape[0] == len(set(shops_df['id'].tolist()))

	def test_tags(self):
		tags_df = pd.read_csv('../data/tags.csv')
		assert tags_df.shape[0] == len(set(tags_df['id'].tolist()))

	def test_products(self):
		products_df = pd.read_csv('../data/products.csv')
		assert products_df.shape[0] == len(set(products_df['id'].tolist()))







###
###	Test class that verifies that the results from the different operations return the same results ###
###	# TODO: verify the element values in the resulting dataframes instead of their shapes
class TestDataframeOperations(object):

	def test_filter_shops_by_location(self):

		shops_df_one = filter_shops_by_location_one()
		shops_df_two = filter_shops_by_location_two()
		shops_df_three = filter_shops_by_location_three()

		assert shops_df_one.shape == shops_df_two.shape
		assert shops_df_one.shape == shops_df_three.shape

	def test_filter_shops_by_ids(self):

		shops_df_one = filter_shops_by_id_one()
		shops_df_two = filter_shops_by_id_two()

		assert shops_df_one.shape == shops_df_two.shape

		
	def test_filter_shops_by_tag_ids(self):

		shops_df_one = filter_shops_by_tag_ids_one()
		shops_df_two = filter_shops_by_tag_ids_two()
		shops_df_three = filter_shops_by_tag_ids_three()
		shops_df_four = filter_shops_by_tag_ids_four()
		shops_df_five = filter_shops_by_tag_ids_five()

		
		assert shops_df_one.shape == shops_df_two.shape
		assert shops_df_one.shape == shops_df_three.shape
		assert shops_df_one.shape == shops_df_four.shape
		assert shops_df_one.shape == shops_df_five.shape

	def test_filter_tag_ids_by_tags(self):

		tags_id_one = filter_tag_ids_by_tags_one()
		tags_id_two = filter_tag_ids_by_tags_two()

		assert tags_id_one == tags_id_two



if __name__ == '__main__':
	import timeit
	

	print '### Test filtering shops by location ###'
	test_func = 'filter_shops_by_location_one'
	print 'mean time for', test_func, ': %f sec' % (
timeit.timeit(test_func+'()', setup='from __main__ import ' + test_func, number=iterations) / float(iterations))

	test_func = 'filter_shops_by_location_two'
	print 'mean time for', test_func, ': %f sec' % (
timeit.timeit(test_func+'()', setup='from __main__ import ' + test_func, number=iterations) / float(iterations))

	test_func = 'filter_shops_by_location_three'
	print 'mean time for', test_func, ': %f sec' % (
timeit.timeit(test_func+'()', setup='from __main__ import ' + test_func, number=iterations) / float(iterations))

	




	print '\n### Test filtering shops by ID ### '
	test_func = 'filter_shops_by_id_one'
	print 'mean time for', test_func, ': %f sec' % (
timeit.timeit(test_func+'()', setup='from __main__ import ' + test_func, number=iterations) / float(iterations))

	test_func = 'filter_shops_by_id_two'
	print 'mean time for', test_func, ': %f sec' % (
timeit.timeit(test_func+'()', setup='from __main__ import ' + test_func, number=iterations) / float(iterations))





	print '\n### Test filtering shops by tag IDs AND location ###'
	test_func = 'filter_shops_by_tag_ids_one'
	print 'mean time for', test_func, ': %f sec' % (
timeit.timeit(test_func+'()', setup='from __main__ import ' + test_func, number=iterations) / float(iterations))

	test_func = 'filter_shops_by_tag_ids_two'
	print 'mean time for', test_func, ': %f sec' % (
timeit.timeit(test_func+'()', setup='from __main__ import ' + test_func, number=iterations) / float(iterations))

	test_func = 'filter_shops_by_tag_ids_three'
	print 'mean time for', test_func, ': %f sec' % (
timeit.timeit(test_func+'()', setup='from __main__ import ' + test_func, number=iterations) / float(iterations))

	test_func = 'filter_shops_by_tag_ids_four'
	print 'mean time for', test_func, ': %f sec' % (
timeit.timeit(test_func+'()', setup='from __main__ import ' + test_func, number=iterations) / float(iterations))

	test_func = 'filter_shops_by_tag_ids_five'
	print 'mean time for', test_func, ': %f sec' % (
timeit.timeit(test_func+'()', setup='from __main__ import ' + test_func, number=iterations) / float(iterations))





	print '\n### Test filtering tag IDs by tags ###'
	test_func = 'filter_tag_ids_by_tags_one'
	print 'mean time for', test_func, ': %f sec' % (
timeit.timeit(test_func+'()', setup='from __main__ import ' + test_func, number=iterations) / float(iterations))

	test_func = 'filter_tag_ids_by_tags_two'
	print 'mean time for', test_func, ': %f sec' % (
timeit.timeit(test_func+'()', setup='from __main__ import ' + test_func, number=iterations) / float(iterations))



