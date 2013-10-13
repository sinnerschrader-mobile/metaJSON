//
//  _S2MSenderJSONObject.m
//
//  Created by MetaJSONParser.
//  Copyright (c) 2013 SinnerSchrader Mobile. All rights reserved.

#import "APIParser.h"
#import "NSString+RegExValidation.h"
#import "S2MSenderJSONObject.h"


@implementation _S2MSenderJSONObject

#pragma mark - factory

+ (S2MSenderJSONObject *)senderWithDictionary:(NSDictionary *)dic withError:(NSError **)error {
    return [[S2MSenderJSONObject alloc] initWithDictionary:dic withError:error];
}


#pragma mark - initialize
- (id)initWithDictionary:(NSDictionary *)dic  withError:(NSError **)error {
    self = [super init];
    if (self) {
        self.senderName = [APIParser stringFromResponseDictionary:dic forKey:@"senderName" acceptNumber:NO acceptNil:NO error:error];
        if (*error) {
            return self;
        }
        self.previewImageURL = [APIParser stringFromResponseDictionary:dic forKey:@"previewImageURL" acceptNumber:NO acceptNil:NO error:error];
        if (*error) {
            return self;
        }
    }
    return self;
}


#pragma mark - getter

#pragma mark - NSCoding
- (void)encodeWithCoder:(NSCoder*)coder {
    [coder encodeObject:self.senderName forKey:@"senderName"];
    [coder encodeObject:self.previewImageURL forKey:@"previewImageURL"];
}
- (id)initWithCoder:(NSCoder *)coder {
    self = [super init];
    self.senderName = [coder decodeObjectForKey:@"senderName"];
    self.previewImageURL = [coder decodeObjectForKey:@"previewImageURL"];
    return self;
}

#pragma mark - Object Info
- (NSDictionary *)propertyDictionary {
    NSMutableDictionary *dic = [[NSMutableDictionary alloc] init];
    if (self.senderName) {
        [dic setObject:self.senderName forKey:@"senderName"];
    }
    if (self.previewImageURL) {
        [dic setObject:self.previewImageURL forKey:@"previewImageURL"];
    }
    return dic;
}
- (NSString *)description {
    return [NSString stringWithFormat:@"%@",[self propertyDictionary]];
}

@end
