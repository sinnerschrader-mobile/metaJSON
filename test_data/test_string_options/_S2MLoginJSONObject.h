//
//  _S2MLoginJSONObject.h
//
//  Created by MetaJSONParser.
//  Copyright (c) 2014 SinnerSchrader Mobile. All rights reserved.

#import <Foundation/Foundation.h>

@class S2MLoginJSONObject;

@interface _S2MLoginJSONObject : NSObject <NSCoding>


@property (nonatomic, strong) NSString *emailString;
@property (nonatomic, strong) NSString *password;

+ (S2MLoginJSONObject *)loginWithDictionary:(NSDictionary *)dic withError:(NSError **)error;
- (id)initWithDictionary:(NSDictionary *)dic withError:(NSError **)error;
- (NSDictionary *)propertyDictionary;

@end

