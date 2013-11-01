//
//  _S2MSenderJSONObject.h
//
//  Created by MetaJSONParser.
//  Copyright (c) 2013 SinnerSchrader Mobile. All rights reserved.

#import <Foundation/Foundation.h>

@class S2MSenderJSONObject;

@interface _S2MSenderJSONObject : NSObject <NSCoding>


@property (nonatomic, strong) NSString *senderName;
@property (nonatomic, strong) NSString *previewImageURL;

+ (S2MSenderJSONObject *)senderWithDictionary:(NSDictionary *)dic withError:(NSError **)error;
- (id)initWithDictionary:(NSDictionary *)dic withError:(NSError **)error;
- (NSDictionary *)propertyDictionary;

@end

