//
//  _FBEUserSuffix.m
//
//  Created by MetaJSONParser.
//  Copyright (c) 2013 SinnerSchrader Mobile. All rights reserved.

#import "FBEAPIParser.h"
#import "NSString+RegExValidation.h"
#import "FBEUserSuffix.h"
#import "FBEUserAddressSuffix.h"
#import "FBEPersonSuffix.h"
#import "FBEMySessionSuffix.h"


@implementation _FBEUserSuffix

#pragma mark - factory

+ (FBEUserSuffix *)userWithDictionary:(NSDictionary *)dic withError:(NSError **)error {
    return [[FBEUserSuffix alloc] initWithDictionary:dic withError:error];
}


#pragma mark - initialize
- (id)initWithDictionary:(NSDictionary *)dic  withError:(NSError **)error {
    self = [super initWithDictionary:dic withError:error];
    if (self) {
        self.email = [FBEAPIParser stringFromResponseDictionary:dic forKey:@"email" acceptNumber:NO acceptNil:YES error:error];
        if (*error) {
            return self;
        }
        if (self.email && [self.email matchesRegExString:@"[A-Z0-9._%+-]+@(?:[A-Z0-9-]+\.)+[A-Z]{2,4}"] == NO) {
            NSDictionary *userInfo = [NSDictionary dictionaryWithObjectsAndKeys:@"email", @"propertyName", @"email", @"key", @"validation error", @"reason", NSStringFromClass([self class]), @"objectClass",nil];
            *error = [NSError errorWithDomain:kFBEErrorDomain_parser code:kFBEErrorDomain_parser_valueIsNotValid userInfo:userInfo];
            NSLog(@"%@", *error);
            return self;
        }
        self.family = [FBEAPIParser arrayFromResponseDictionary:dic forKey:@"family" acceptNil:NO error:error];
        if (*error) {
            return self;
        }
        self.userID = [FBEAPIParser stringFromResponseDictionary:dic forKey:@"userID" acceptNumber:NO acceptNil:NO error:error];
        if (*error) {
            return self;
        }
        NSDictionary *tmpAddress = [FBEAPIParser dictionaryFromResponseDictionary:dic forKey:@"address" acceptNil:NO error:error];
        if (*error) {
            return self;
        }
        if (tmpAddress) {
            self.address= [[FBEUserAddressSuffix alloc] initWithDictionary:tmpAddress withError:error];
            if (*error) {
                return self;
            }
        }
        NSDictionary *tmpSession = [FBEAPIParser dictionaryFromResponseDictionary:dic forKey:@"session" acceptNil:NO error:error];
        if (*error) {
            return self;
        }
        if (tmpSession) {
            self.session= [[FBEMySessionSuffix alloc] initWithDictionary:tmpSession withError:error];
            if (*error) {
                return self;
            }
        }
    }
    return self;
}


#pragma mark - getter
- (FBEPersonSuffix *)personInFamilyAtIndex:(NSUInteger)index withError:(NSError **)error {
    NSDictionary *tmpFamilyDic = [FBEAPIParser dictionaryFromResponseArray:self.family atIndex:index acceptNil:NO error:error];
    if (*error) {
        return nil;
    }
    FBEPersonSuffix *tmpFamily = nil;
    if (tmpFamilyDic == nil) {
        return nil;
    }
    if (tmpFamilyDic) {
        tmpFamily= [[FBEPersonSuffix alloc] initWithDictionary:tmpFamilyDic withError:error];
        if (*error) {
            return nil;
        }
    }
    return tmpFamily;
}
- (FBEUserAddressSuffix *)userAddressInFamilyAtIndex:(NSUInteger)index withError:(NSError **)error {
    NSDictionary *tmpFamilyDic = [FBEAPIParser dictionaryFromResponseArray:self.family atIndex:index acceptNil:NO error:error];
    if (*error) {
        return nil;
    }
    FBEUserAddressSuffix *tmpFamily = nil;
    if (tmpFamilyDic == nil) {
        return nil;
    }
    if (tmpFamilyDic) {
        tmpFamily= [[FBEUserAddressSuffix alloc] initWithDictionary:tmpFamilyDic withError:error];
        if (*error) {
            return nil;
        }
    }
    return tmpFamily;
}
- (NSString *)stringInFamilyAtIndex:(NSUInteger)index withError:(NSError **)error {
    NSString *tmpFamily = [FBEAPIParser stringFromResponseArray:self.family atIndex:index acceptNil:NO error:error];
    if (*error) {
        return nil;
    }
    return tmpFamily;
}

#pragma mark - NSCoding
- (void)encodeWithCoder:(NSCoder*)coder {
    [super encodeWithCoder:coder];
    [coder encodeObject:self.email forKey:@"email"];
    [coder encodeObject:self.family forKey:@"family"];
    [coder encodeObject:self.userID forKey:@"userID"];
    [coder encodeObject:self.address forKey:@"address"];
    [coder encodeObject:self.session forKey:@"session"];
}
- (id)initWithCoder:(NSCoder *)coder {
    self = [super initWithCoder:coder];
    self.email = [coder decodeObjectForKey:@"email"];
    self.family = [coder decodeObjectForKey:@"family"];
    self.userID = [coder decodeObjectForKey:@"userID"];
    self.address = [coder decodeObjectForKey:@"address"];
    self.session = [coder decodeObjectForKey:@"session"];
    return self;
}

#pragma mark - Object Info
- (NSDictionary *)propertyDictionary {
    NSDictionary *parentDic = [super propertyDictionary];
    NSMutableDictionary *dic = [[NSMutableDictionary alloc] initWithDictionary:parentDic];
    if (self.email) {
        [dic setObject:self.email forKey:@"email"];
    }
    if (self.family) {
        [dic setObject:self.family forKey:@"family"];
    }
    if (self.userID) {
        [dic setObject:self.userID forKey:@"userID"];
    }
    if (self.address) {
        [dic setObject:[self.address propertyDictionary] forKey:@"address"];
    }
    if (self.session) {
        [dic setObject:[self.session propertyDictionary] forKey:@"session"];
    }
    return dic;
}
- (NSString *)description {
    return [NSString stringWithFormat:@"%@",[self propertyDictionary]];
}

@end
