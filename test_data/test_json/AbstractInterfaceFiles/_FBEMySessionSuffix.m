//
//  _FBEMySessionSuffix.m
//
//  Created by MetaJSONParser.
//  Copyright (c) 2013 SinnerSchrader Mobile. All rights reserved.

#import "FBEAPIParser.h"
#import "NSString+RegExValidation.h"
#import "FBEMySessionSuffix.h"


@implementation _FBEMySessionSuffix

#pragma mark - factory

+ (FBEMySessionSuffix *)mySessionWithDictionary:(NSDictionary *)dic withError:(NSError **)error {
    return [[FBEMySessionSuffix alloc] initWithDictionary:dic withError:error];
}


#pragma mark - initialize
- (id)initWithDictionary:(NSDictionary *)dic  withError:(NSError **)error {
    self = [super init];
    if (self) {
        self.sessionID = [FBEAPIParser stringFromResponseDictionary:dic forKey:@"sessionID" acceptNumber:NO acceptNil:NO error:error];
        if (*error) {
            return self;
        }
        if (self.sessionID.length > 50) {
            NSDictionary *userInfo = [NSDictionary dictionaryWithObjectsAndKeys:@"sessionID", @"propertyName", @"sessionID", @"key", @"validation error", @"reason", NSStringFromClass([self class]), @"objectClass",nil];
            *error = [NSError errorWithDomain:kFBEErrorDomain_parser code:kFBEErrorDomain_parser_valueIsNotValid userInfo:userInfo];
            NSLog(@"%@", *error);
            return self;
        }
        if (self.sessionID.length < 20) {
            NSDictionary *userInfo = [NSDictionary dictionaryWithObjectsAndKeys:@"sessionID", @"propertyName", @"sessionID", @"key", @"validation error", @"reason", NSStringFromClass([self class]), @"objectClass",nil];
            *error = [NSError errorWithDomain:kFBEErrorDomain_parser code:kFBEErrorDomain_parser_valueIsNotValid userInfo:userInfo];
            NSLog(@"%@", *error);
            return self;
        }
        self.expirationDate = [FBEAPIParser dateWithTimeIntervalFromResponseDictionary:dic forKey:@"expirationDate" acceptNil:NO error:error];
        if (*error) {
            return self;
        }
        if ([self.expirationDate timeIntervalSince1970] > 183759284) {
            NSDictionary *userInfo = [NSDictionary dictionaryWithObjectsAndKeys:@"expirationDate", @"propertyName", @"expirationDate", @"key", @"validation error", @"reason", NSStringFromClass([self class]), @"objectClass",nil];
            *error = [NSError errorWithDomain:kFBEErrorDomain_parser code:kFBEErrorDomain_parser_valueIsNotValid userInfo:userInfo];
            NSLog(@"%@", *error);
            return self;
        }
    }
    return self;
}


#pragma mark - getter

#pragma mark - NSCoding
- (void)encodeWithCoder:(NSCoder*)coder {
    [coder encodeObject:self.sessionID forKey:@"sessionID"];
    [coder encodeObject:self.expirationDate forKey:@"expirationDate"];
}
- (id)initWithCoder:(NSCoder *)coder {
    self = [super init];
    self.sessionID = [coder decodeObjectForKey:@"sessionID"];
    self.expirationDate = [coder decodeObjectForKey:@"expirationDate"];
    return self;
}

#pragma mark - Object Info
- (NSDictionary *)propertyDictionary {
    NSMutableDictionary *dic = [[NSMutableDictionary alloc] init];
    if (self.sessionID) {
        [dic setObject:self.sessionID forKey:@"sessionID"];
    }
    if (self.expirationDate) {
        [dic setObject:[NSNumber numberWithInteger:[[NSNumber numberWithDouble:[self.expirationDate timeIntervalSince1970]] longValue]] forKey:@"expirationDate"];
    }
    return dic;
}
- (NSString *)description {
    return [NSString stringWithFormat:@"%@",[self propertyDictionary]];
}

@end
