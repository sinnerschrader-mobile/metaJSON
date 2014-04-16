//
//  _SubClassJSONObject.h
//
//  Created by MetaJSONParser.
//  Copyright (c) 2014 SinnerSchrader Mobile. All rights reserved.

#import <Foundation/Foundation.h>
#import ".h"

@class SubClassJSONObject;

@interface _SubClassJSONObject : 

@property (nonatomic, strong) NSString *name;

+ (SubClassJSONObject *)subClassWithDictionary:(NSDictionary *)dic withError:(NSError **)error;
- (id)initWithDictionary:(NSDictionary *)dic withError:(NSError **)error;

@end
