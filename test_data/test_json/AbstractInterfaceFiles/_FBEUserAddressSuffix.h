//
//  _FBEUserAddressSuffix.h
//
//  Created by MetaJSONParser.
//  Copyright (c) 2013 SinnerSchrader Mobile. All rights reserved.

#import <Foundation/Foundation.h>

@class FBEUserAddressSuffix;

@interface _FBEUserAddressSuffix : NSObject <NSCoding>


@property (nonatomic, strong) NSString *street;
@property (nonatomic, strong) NSString *houseNumber;
@property (nonatomic, strong) NSString *additionalAddress;
@property (nonatomic, strong) NSString *City;
@property (nonatomic, strong) NSString *Country;
@property (nonatomic, strong) NSString *zipCode;

+ (FBEUserAddressSuffix *)userAddressWithDictionary:(NSDictionary *)dic withError:(NSError **)error;
- (id)initWithDictionary:(NSDictionary *)dic withError:(NSError **)error;
- (NSDictionary *)propertyDictionary;

@end

