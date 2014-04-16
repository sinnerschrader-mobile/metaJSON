//
//  _SubClassJSONObject.m
//
//  Created by MetaJSONParser.
//  Copyright (c) 2014 SinnerSchrader Mobile. All rights reserved.

#import "APIParser.h"
#import "NSString+RegExValidation.h"
#import "SubClassJSONObject.h"


@implementation _SubClassJSONObject

#pragma mark - factory

+ (SubClassJSONObject *)subClassWithDictionary:(NSDictionary *)dic withError:(NSError **)error
{
    return [[SubClassJSONObject alloc] initWithDictionary:dic withError:error];
}

#pragma mark - initialize
- (id)initWithDictionary:(NSDictionary *)dic  withError:(NSError **)error
{
    self = [super initWithDictionary:dic withError:error];
    if (self) {
        self.name = [APIParser stringFromResponseDictionary:dic forKey:@"name" acceptNumber:NO acceptNil:YES error:error];
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
    [coder encodeObject:self.name forKey:@"name"];
}

- (id)initWithCoder:(NSCoder *)coder
{
    self = [super initWithCoder:coder];
    self.name = [coder decodeObjectForKey:@"name"];
    return self;
}

#pragma mark - Object Info
- (NSDictionary *)propertyDictionary
{
    NSMutableDictionary *dic = [[super propertyDictionary] mutableCopy];
    if (self.name) {
        [dic setObject:self.name forKey:@"name"];
    }
    return dic;
}


@end
