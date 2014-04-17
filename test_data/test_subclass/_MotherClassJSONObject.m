//
//  _MotherClassJSONObject.m
//
//  Created by MetaJSONParser.
//  Copyright (c) 2014 SinnerSchrader Mobile. All rights reserved.

#import "APIParser.h"
#import "NSString+RegExValidation.h"
#import "MotherClassJSONObject.h"


@implementation _MotherClassJSONObject

#pragma mark - factory

+ (MotherClassJSONObject *)motherClassWithDictionary:(NSDictionary *)dic withError:(NSError **)error
{
    return [[MotherClassJSONObject alloc] initWithDictionary:dic withError:error];
}

#pragma mark - initialize
- (id)initWithDictionary:(NSDictionary *)dic  withError:(NSError **)error
{
    self = [super init];
    if (self) {
        self.metaId = [APIParser stringFromResponseDictionary:dic forKey:@"id" acceptNumber:NO acceptNil:NO error:error];
        if (*error) {
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
    [coder encodeObject:self.metaId forKey:@"id"];
}

- (id)initWithCoder:(NSCoder *)coder
{
    self = [super initWithCoder:coder];
    self.metaId = [coder decodeObjectForKey:@"id"];
    return self;
}

#pragma mark - Object Info
- (NSDictionary *)propertyDictionary
{
    NSMutableDictionary *dic = [[NSMutableDictionary alloc] init];
    if (self.metaId) {
        [dic setObject:self.metaId forKey:@"id"];
    }
    return dic;
}

- (NSString *)description
{
    return [[self propertyDictionary] description];
}

@end
