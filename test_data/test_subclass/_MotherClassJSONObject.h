//
//  _MotherClassJSONObject.h
//
//  Created by MetaJSONParser.
//  Copyright (c) 2014 SinnerSchrader Mobile. All rights reserved.

#import <Foundation/Foundation.h>

@class MotherClassJSONObject;

@interface _MotherClassJSONObject : NSObject <NSCoding>

@property (nonatomic, strong) NSString *id;

+ (MotherClassJSONObject *)motherClassWithDictionary:(NSDictionary *)dic withError:(NSError **)error;
- (id)initWithDictionary:(NSDictionary *)dic withError:(NSError **)error;
- (NSDictionary *)propertyDictionary;

@end
