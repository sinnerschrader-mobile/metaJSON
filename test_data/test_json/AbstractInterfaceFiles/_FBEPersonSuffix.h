//
//  _FBEPersonSuffix.h
//
//  Created by MetaJSONParser.
//  Copyright (c) 2013 SinnerSchrader Mobile. All rights reserved.

#import <Foundation/Foundation.h>

@class FBEPersonSuffix;

@interface _FBEPersonSuffix : NSObject <NSCoding>


@property (nonatomic, strong) NSString *firstName;
@property (nonatomic, strong) NSString *lastName;

+ (FBEPersonSuffix *)personWithDictionary:(NSDictionary *)dic withError:(NSError **)error;
- (id)initWithDictionary:(NSDictionary *)dic withError:(NSError **)error;
- (NSDictionary *)propertyDictionary;

@end

