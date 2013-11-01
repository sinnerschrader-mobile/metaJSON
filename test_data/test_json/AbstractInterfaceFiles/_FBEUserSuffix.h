//
//  _FBEUserSuffix.h
//
//  Created by MetaJSONParser.
//  Copyright (c) 2013 SinnerSchrader Mobile. All rights reserved.

#import <Foundation/Foundation.h>
#import "FBEPersonSuffix.h"

@class FBEUserAddressSuffix;
@class FBEPersonSuffix;
@class FBEMySessionSuffix;

@class FBEUserSuffix;

@interface _FBEUserSuffix : FBEPersonSuffix


@property (nonatomic, strong) NSString *email;
@property (nonatomic, strong) NSArray *family;
@property (nonatomic, strong) NSString *userID;
@property (nonatomic, strong) FBEUserAddressSuffix *address;
@property (nonatomic, strong) FBEMySessionSuffix *session;

+ (FBEUserSuffix *)userWithDictionary:(NSDictionary *)dic withError:(NSError **)error;
- (id)initWithDictionary:(NSDictionary *)dic withError:(NSError **)error;
- (NSDictionary *)propertyDictionary;
- (FBEPersonSuffix *)personInFamilyAtIndex:(NSUInteger)index withError:(NSError **)error;
- (FBEUserAddressSuffix *)userAddressInFamilyAtIndex:(NSUInteger)index withError:(NSError **)error;
- (NSString *)stringInFamilyAtIndex:(NSUInteger)index withError:(NSError **)error;

@end

