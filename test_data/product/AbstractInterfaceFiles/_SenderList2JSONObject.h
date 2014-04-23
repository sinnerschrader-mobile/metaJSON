//
//  _SenderList2JSONObject.h
//
//  Created by MetaJSONParser.
//  Copyright (c) 2014 SinnerSchrader Mobile. All rights reserved.

#import <Foundation/Foundation.h>
#import "SenderListJSONObject.h"

@class SenderList2JSONObject;

@interface _SenderList2JSONObject : SenderListJSONObject


// the title of sender list
@property (nonatomic, strong) NSString *listSubTitle;

+ (SenderList2JSONObject *)senderList2WithDictionary:(NSDictionary *)dic withError:(NSError **)error;
- (id)initWithDictionary:(NSDictionary *)dic withError:(NSError **)error;
- (NSDictionary *)propertyDictionary;

@end

