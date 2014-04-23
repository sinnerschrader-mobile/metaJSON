//
//  _ProductDetailJSONObject.h
//
//  Created by MetaJSONParser.
//  Copyright (c) 2014 SinnerSchrader Mobile. All rights reserved.

#import <Foundation/Foundation.h>

@class SenderGroupJSONObject;

@class ProductDetailJSONObject;

@interface _ProductDetailJSONObject : NSObject <NSCoding>


// the title of product
@property (nonatomic, strong) id title;
// the type of product
@property (nonatomic, strong) NSNumber *type;
// teaser image url of product
@property (nonatomic, strong) NSString *teaserURL;
// download speed (Mbit/s)
@property (nonatomic, strong) id download;
// upload speed (Mbit/s)
@property (nonatomic, strong) id upload;
// telephone Flatrate option string
@property (nonatomic, strong) NSString *telephoneFlatrate;
@property (nonatomic, strong) SenderGroupJSONObject *senderInfo;
@property (nonatomic, assign) BOOL includeHardware;
@property (nonatomic, strong) id anyProperty;
@property (nonatomic, strong) NSNumber *advantage;

+ (ProductDetailJSONObject *)ProductDetailWithDictionary:(NSDictionary *)dic withError:(NSError **)error;
- (id)initWithDictionary:(NSDictionary *)dic withError:(NSError **)error;
- (NSDictionary *)propertyDictionary;
- (NSString *)titleAsTitleString:(NSError **)error;
- (NSString *)titleAsString:(NSError **)error;
- (NSNumber *)downloadAsNumber:(NSError **)error;
- (NSString *)downloadAsString:(NSError **)error;
- (NSNumber *)uploadAsNumber:(NSError **)error;
- (NSString *)uploadAsString:(NSError **)error;

@end

