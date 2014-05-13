//
//  _S2MLoginJSONObject.m
//
//  Created by MetaJSONParser.
//  Copyright (c) 2014 SinnerSchrader Mobile. All rights reserved.

#import "S2MAPIParser.h"
#import "NSString+RegExValidation.h"
#import "S2MLoginJSONObject.h"


@implementation _S2MLoginJSONObject

#pragma mark - factory

+ (S2MLoginJSONObject *)loginWithDictionary:(NSDictionary *)dic withError:(NSError **)error
{
    return [[S2MLoginJSONObject alloc] initWithDictionary:dic withError:error];
}

#pragma mark - initialize
- (id)initWithDictionary:(NSDictionary *)dic  withError:(NSError **)error
{
    self = [super init];
    if (self) {
        self.emailString = [S2MAPIParser stringFromResponseDictionary:dic forKey:@"emailString" acceptNumber:NO acceptNil:YES error:error];
        if (*error) {
            return self;
        }
        if (self.emailString && [self.emailString matchesRegExString:@"[a-z0-9!#$%&'*+/=?^_`{|}~-](?:\\.[a-z0-9!#$%&'*/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"] == NO) {
            NSDictionary *userInfo = @{@"propertyName" : @"emailString",
                                       @"key" : @"emailString",
                                       @"reason" : @"validation error",
                                       @"objectClass" : NSStringFromClass([self class])
                                       };
            *error = [NSError errorWithDomain:kS2MErrorDomain_parser code:kS2MErrorDomain_parser_valueIsNotValid userInfo:userInfo];
            NSLog(@"%@", *error);
            return self;
        }
        self.password = [S2MAPIParser stringFromResponseDictionary:dic forKey:@"password" acceptNumber:NO acceptNil:YES error:error];
        if (*error) {
            return self;
        }
        if (self.password.length > 12) {
            NSDictionary *userInfo = @{@"propertyName" : @"password",
                                       @"key" : @"password",
                                       @"reason" : @"max length validation error",
                                       @"objectClass" : NSStringFromClass([self class])
                                       };
            *error = [NSError errorWithDomain:kS2MErrorDomain_parser code:kS2MErrorDomain_parser_valueIsNotValid userInfo:userInfo];
            NSLog(@"%@", *error);
            return self;
        }
        if (self.password.length < 3) {
            NSDictionary *userInfo = @{@"propertyName" : @"password",
                                       @"key" : @"password",
                                       @"reason" : @"min length validation error",
                                       @"objectClass" : NSStringFromClass([self class])
                                       };
            *error = [NSError errorWithDomain:kS2MErrorDomain_parser code:kS2MErrorDomain_parser_valueIsNotValid userInfo:userInfo];
            NSLog(@"%@", *error);
            return self;
        }
    }
    return self;
}

#pragma mark - getter

#pragma mark - NSCoding

- (void)encodeWithCoder:(NSCoder*)coder
{
    [super encodeWithCoder:coder];
    [coder encodeObject:self.emailString forKey:@"emailString"];
    [coder encodeObject:self.password forKey:@"password"];
}

- (id)initWithCoder:(NSCoder *)coder
{
    self = [super initWithCoder:coder];
    self.emailString = [coder decodeObjectForKey:@"emailString"];
    self.password = [coder decodeObjectForKey:@"password"];
    return self;
}

#pragma mark - Object Info
- (NSDictionary *)propertyDictionary
{
    NSMutableDictionary *dic = [[NSMutableDictionary alloc] init];
    if (self.emailString) {
        [dic setObject:self.emailString forKey:@"emailString"];
    }
    if (self.password) {
        [dic setObject:self.password forKey:@"password"];
    }
    return dic;
}

- (NSString *)description
{
    return [[self propertyDictionary] description];
}

@end
