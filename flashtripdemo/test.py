image_list = ['https://ccm.ddcdn.com/ext/photo-w/12/9b/0d/9d/blues-luxury-suite-master.jpg',
              'https://ccm.ddcdn.com/ext/photo-w/12/9b/0a/7d/mozart-suite-vrtba-garden.jpg',
              'https://ccm.ddcdn.com/ext/photo-w/12/9b/0d/98/blues-luxury-suite-living.jpg',
              'https://ccm.ddcdn.com/ext/photo-w/12/9b/08/19/junior-suite-bach-garden.jpg',
              'https://ccm.ddcdn.com/ext/photo-w/12/9b/08/f2/junior-suite-2-double.jpg',
              'https://ccm.ddcdn.com/ext/photo-w/12/9b/07/2d/deluxe-room-contemporary.jpg',
              'https://ccm.ddcdn.com/ext/photo-w/12/9b/08/b6/beethoven-suite-master.jpg',
              'https://ccm.ddcdn.com/ext/photo-w/12/9b/0a/78/mozart-two-bedroom-luxury.jpg',
              'https://ccm.ddcdn.com/ext/photo-w/12/9b/11/5a/screening-room-u-shape.jpg',
              'https://ccm.ddcdn.com/ext/photo-w/12/9b/0a/6d/mozart-two-bedroom-luxury.jpg',
              'https://ccm.ddcdn.com/ext/photo-w/12/9b/07/9c/luxury-one-bedroom-suite.jpg',
              'https://ccm.ddcdn.com/ext/photo-w/12/9b/09/78/smetana-one-bedroom-suite.jpg',
              'https://ccm.ddcdn.com/ext/photo-w/12/9b/08/ad/beethoven-2-bedroom-suite.jpg',
              'https://ccm.ddcdn.com/ext/photo-w/12/9b/09/7e/smetana-one-bedroom-suite.jpg',
              'https://ccm.ddcdn.com/ext/photo-w/12/9b/0a/82/mozart-suite-master-bedroom.jpg',
              'https://ccm.ddcdn.com/ext/photo-w/12/9b/0a/91/mozart-two-bedroom-luxury.jpg',
              'https://ccm.ddcdn.com/ext/photo-w/12/9b/0d/9d/blues-luxury-suite-master.jpg',
              'https://ccm.ddcdn.com/ext/photo-w/12/9b/0a/7d/mozart-suite-vrtba-garden.jpg',
              'https://ccm.ddcdn.com/ext/photo-w/12/9b/0d/98/blues-luxury-suite-living.jpg',
              'https://ccm.ddcdn.com/ext/photo-w/12/9b/08/19/junior-suite-bach-garden.jpg',
              'https://ccm.ddcdn.com/ext/photo-w/12/9b/08/f2/junior-suite-2-double.jpg',
              'https://ccm.ddcdn.com/ext/photo-w/12/9b/07/2d/deluxe-room-contemporary.jpg',
              'https://ccm.ddcdn.com/ext/photo-w/12/9b/08/b6/beethoven-suite-master.jpg',
              'https://ccm.ddcdn.com/ext/photo-w/12/9b/0a/78/mozart-two-bedroom-luxury.jpg',
              'https://ccm.ddcdn.com/ext/photo-w/12/9b/11/5a/screening-room-u-shape.jpg',
              'https://ccm.ddcdn.com/ext/photo-w/12/9b/0a/6d/mozart-two-bedroom-luxury.jpg',
              'https://ccm.ddcdn.com/ext/photo-w/12/9b/07/9c/luxury-one-bedroom-suite.jpg',
              'https://ccm.ddcdn.com/ext/photo-w/12/9b/09/78/smetana-one-bedroom-suite.jpg',
              'https://ccm.ddcdn.com/ext/photo-w/12/9b/08/ad/beethoven-2-bedroom-suite.jpg',
              'https://ccm.ddcdn.com/ext/photo-w/12/9b/09/7e/smetana-one-bedroom-suite.jpg',
              'https://ccm.ddcdn.com/ext/photo-w/12/9b/0a/82/mozart-suite-master-bedroom.jpg',
              'https://ccm.ddcdn.com/ext/photo-w/12/9b/0a/91/mozart-two-bedroom-luxury.jpg']

image_list = list(set(image_list))
image_dict = {}
for image in image_list:
    image_split = image.split('/')
    # print(image_split[-2] + image_split[-1])
    image_dict[image_split[-2] + image_split[-2]] = image
print(list(image_dict.values()))
