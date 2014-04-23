//
//  _SenderList2JSONObject.m
//
//  Created by MetaJSONParser.
//  Copyright (c) 2014 SinnerSchrader Mobile. All rights reserved.

#import "APIParser.h"
#import "NSString+RegExValidation.h"
#import "SenderList2JSONObject.h"


@implementation _SenderList2JSONObject

#pragma mark - factory

+ (SenderList2JSONObject *)senderList2WithDictionary:(NSDictionary *)dic withError:(NSError **)error {
    return [[SenderList2JSONObject alloc] initWithDictionary:dic withError:error];
}


#pragma mark - initialize
- (id)initWithDictionary:(NSDictionary *)dic  withError:(NSError **)error {
    self = [super initWithDictionary:dic withError:error];
    if (self) {
        self.listSubTitle = [APIParser stringFromResponseDictionary:dic forKey:@"listSubTitle" acceptNumber:NO acceptNil:NO error:error];
        if (*error) {
            return self;
        }
    }
    return self;
}


#pragma mark - getter

#pragma mark - NSCoding
- (void)encodeWithCoder:(NSCoder*)coder {
    [super encodeWithCoder:coder];
    [coder encodeObject:self.listSubTitle forKey:@"listSubTitle"];
}
- (id)initWithCoder:(NSCoder *)coder {
    self = [super initWithCoder:coder];
    self.listSubTitle = [coder decodeObjectForKey:@"listSubTitle"];
    return self;
}

#pragma mark - Object Info
- (NSDictionary *)propertyDictionary {
    NSDictionary *parentDic = [super propertyDictionary];
    NSMutableDictionary *dic = [[NSMutableDictionary alloc] initWithDictionary:parentDic];
    if (self.listSubTitle) {
        [dic setObject:self.listSubTitle forKey:@"listSubTitle"];
    }
    return dic;
}
- (NSString *)description {
    return [NSString stringWithFormat:@"%@",[self propertyDictionary]];
}

@end
