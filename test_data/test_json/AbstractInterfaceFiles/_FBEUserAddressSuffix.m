//
//  _FBEUserAddressSuffix.m
//
//  Created by MetaJSONParser.
//  Copyright (c) 2013 SinnerSchrader Mobile. All rights reserved.

#import "FBEAPIParser.h"
#import "NSString+RegExValidation.h"
#import "FBEUserAddressSuffix.h"


@implementation _FBEUserAddressSuffix

#pragma mark - factory

+ (FBEUserAddressSuffix *)userAddressWithDictionary:(NSDictionary *)dic withError:(NSError **)error {
    return [[FBEUserAddressSuffix alloc] initWithDictionary:dic withError:error];
}


#pragma mark - initialize
- (id)initWithDictionary:(NSDictionary *)dic  withError:(NSError **)error {
    self = [super init];
    if (self) {
        self.street = [FBEAPIParser stringFromResponseDictionary:dic forKey:@"street" acceptNumber:NO acceptNil:NO error:error];
        if (*error) {
            return self;
        }
        self.houseNumber = [FBEAPIParser stringFromResponseDictionary:dic forKey:@"houseNumber" acceptNumber:NO acceptNil:NO error:error];
        if (*error) {
            return self;
        }
        self.additionalAddress = [FBEAPIParser stringFromResponseDictionary:dic forKey:@"additionalAddress" acceptNumber:NO acceptNil:YES error:error];
        if (*error) {
            return self;
        }
        self.City = [FBEAPIParser stringFromResponseDictionary:dic forKey:@"City" acceptNumber:NO acceptNil:NO error:error];
        if (*error) {
            return self;
        }
        self.Country = [FBEAPIParser stringFromResponseDictionary:dic forKey:@"Country" acceptNumber:NO acceptNil:NO error:error];
        if (*error) {
            return self;
        }
        self.zipCode = [FBEAPIParser stringFromResponseDictionary:dic forKey:@"zipCode" acceptNumber:NO acceptNil:NO error:error];
        if (*error) {
            return self;
        }
    }
    return self;
}


#pragma mark - getter

#pragma mark - NSCoding
- (void)encodeWithCoder:(NSCoder*)coder {
    [coder encodeObject:self.street forKey:@"street"];
    [coder encodeObject:self.houseNumber forKey:@"houseNumber"];
    [coder encodeObject:self.additionalAddress forKey:@"additionalAddress"];
    [coder encodeObject:self.City forKey:@"City"];
    [coder encodeObject:self.Country forKey:@"Country"];
    [coder encodeObject:self.zipCode forKey:@"zipCode"];
}
- (id)initWithCoder:(NSCoder *)coder {
    self = [super init];
    self.street = [coder decodeObjectForKey:@"street"];
    self.houseNumber = [coder decodeObjectForKey:@"houseNumber"];
    self.additionalAddress = [coder decodeObjectForKey:@"additionalAddress"];
    self.City = [coder decodeObjectForKey:@"City"];
    self.Country = [coder decodeObjectForKey:@"Country"];
    self.zipCode = [coder decodeObjectForKey:@"zipCode"];
    return self;
}

#pragma mark - Object Info
- (NSDictionary *)propertyDictionary {
    NSMutableDictionary *dic = [[NSMutableDictionary alloc] init];
    if (self.street) {
        [dic setObject:self.street forKey:@"street"];
    }
    if (self.houseNumber) {
        [dic setObject:self.houseNumber forKey:@"houseNumber"];
    }
    if (self.additionalAddress) {
        [dic setObject:self.additionalAddress forKey:@"additionalAddress"];
    }
    if (self.City) {
        [dic setObject:self.City forKey:@"City"];
    }
    if (self.Country) {
        [dic setObject:self.Country forKey:@"Country"];
    }
    if (self.zipCode) {
        [dic setObject:self.zipCode forKey:@"zipCode"];
    }
    return dic;
}
- (NSString *)description {
    return [NSString stringWithFormat:@"%@",[self propertyDictionary]];
}

@end
