//
//  _FBEPersonSuffix.m
//
//  Created by MetaJSONParser.
//  Copyright (c) 2013 SinnerSchrader Mobile. All rights reserved.

#import "FBEAPIParser.h"
#import "NSString+RegExValidation.h"
#import "FBEPersonSuffix.h"


@implementation _FBEPersonSuffix

#pragma mark - factory

+ (FBEPersonSuffix *)personWithDictionary:(NSDictionary *)dic withError:(NSError **)error {
    return [[FBEPersonSuffix alloc] initWithDictionary:dic withError:error];
}


#pragma mark - initialize
- (id)initWithDictionary:(NSDictionary *)dic  withError:(NSError **)error {
    self = [super init];
    if (self) {
        self.firstName = [FBEAPIParser stringFromResponseDictionary:dic forKey:@"firstName" acceptNumber:NO acceptNil:NO error:error];
        if (*error) {
            return self;
        }
        self.lastName = [FBEAPIParser stringFromResponseDictionary:dic forKey:@"lastName" acceptNumber:NO acceptNil:NO error:error];
        if (*error) {
            return self;
        }
    }
    return self;
}


#pragma mark - getter

#pragma mark - NSCoding
- (void)encodeWithCoder:(NSCoder*)coder {
    [coder encodeObject:self.firstName forKey:@"firstName"];
    [coder encodeObject:self.lastName forKey:@"lastName"];
}
- (id)initWithCoder:(NSCoder *)coder {
    self = [super init];
    self.firstName = [coder decodeObjectForKey:@"firstName"];
    self.lastName = [coder decodeObjectForKey:@"lastName"];
    return self;
}

#pragma mark - Object Info
- (NSDictionary *)propertyDictionary {
    NSMutableDictionary *dic = [[NSMutableDictionary alloc] init];
    if (self.firstName) {
        [dic setObject:self.firstName forKey:@"firstName"];
    }
    if (self.lastName) {
        [dic setObject:self.lastName forKey:@"lastName"];
    }
    return dic;
}
- (NSString *)description {
    return [NSString stringWithFormat:@"%@",[self propertyDictionary]];
}

@end
