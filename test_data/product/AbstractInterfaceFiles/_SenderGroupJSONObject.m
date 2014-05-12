//
//  _SenderGroupJSONObject.m
//
//  Created by MetaJSONParser.
//  Copyright (c) 2014 SinnerSchrader Mobile. All rights reserved.

#import "APIParser.h"
#import "NSString+RegExValidation.h"
#import "SenderGroupJSONObject.h"
#import "SenderListJSONObject.h"
#import "SenderList2JSONObject.h"



@implementation _SenderGroupJSONObject

#pragma mark - factory

+ (SenderGroupJSONObject *)senderGroupWithDictionary:(NSDictionary *)dic withError:(NSError **)error
{
    return [[SenderGroupJSONObject alloc] initWithDictionary:dic withError:error];
}


#pragma mark - initialize
- (id)initWithDictionary:(NSDictionary *)dic  withError:(NSError **)error
{
    self = [super init];
    if (self) {
        self.digitalSenders = [APIParser arrayFromResponseDictionary:dic forKey:@"digitalSenders" acceptNil:YES error:error];
        if (*error) {
            return self;
        }
        self.HDOptions = [APIParser arrayFromResponseDictionary:dic forKey:@"HDOptions" acceptNil:YES error:error];
        if (*error) {
            return self;
        }
        self.DTVHighlights = [APIParser arrayFromResponseDictionary:dic forKey:@"DTVHighlights" acceptNil:YES error:error];
        if (*error) {
            return self;
        }
        if (self.DTVHighlights.count > 6) {
            NSDictionary *userInfo = @{@"propertyName" : @"DTVHighlights",
                                     @"key" : @"DTVHighlights",
                                     @"reason" : @"max count validation error",
                                     @"objectClass" : NSStringFromClass([self class])
                                     };
            *error = [NSError errorWithDomain:kErrorDomain_parser code:kErrorDomain_parser_valueIsNotValid userInfo:userInfo];
            NSLog(@"%@", *error);
            return self;
        }
        if (self.DTVHighlights.count < 2) {
            NSDictionary *userInfo = @{@"propertyName" : @"DTVHighlights",
                                     @"key" : @"DTVHighlights",
                                     @"reason" : @"min count validation error",
                                     @"objectClass" : NSStringFromClass([self class])
                                     };
            *error = [NSError errorWithDomain:kErrorDomain_parser code:kErrorDomain_parser_valueIsNotValid userInfo:userInfo];
            NSLog(@"%@", *error);
            return self;
        }
        self.IPTVSenders = [APIParser arrayFromResponseDictionary:dic forKey:@"IPTVSenders" acceptNil:YES error:error];
        if (*error) {
            return self;
        }
        if (self.IPTVSenders.count > 6) {
            NSDictionary *userInfo = @{@"propertyName" : @"IPTVSenders",
                                     @"key" : @"IPTVSenders",
                                     @"reason" : @"max count validation error",
                                     @"objectClass" : NSStringFromClass([self class])
                                     };
            *error = [NSError errorWithDomain:kErrorDomain_parser code:kErrorDomain_parser_valueIsNotValid userInfo:userInfo];
            NSLog(@"%@", *error);
            return self;
        }
        if (self.IPTVSenders.count < 2) {
            NSDictionary *userInfo = @{@"propertyName" : @"IPTVSenders",
                                                 @"key" : @"IPTVSenders",
                                                 @"reason" : @"min count validation error",
                                                 @"objectClass" : NSStringFromClass([self class])
                                                 };
            *error = [NSError errorWithDomain:kErrorDomain_parser code:kErrorDomain_parser_valueIsNotValid userInfo:userInfo];
            NSLog(@"%@", *error);
            return self;
        }
    }
    return self;
}

#pragma mark - getter

- (SenderListJSONObject *)senderListInDigitalSendersAtIndex:(NSUInteger)index withError:(NSError **)error
{
    NSDictionary *tmpDigitalSendersDic = [APIParser dictionaryFromResponseArray:self.digitalSenders atIndex:index acceptNil:YES error:error];
    if (*error) {
        return nil;
    }
    SenderListJSONObject *tmpDigitalSenders = nil;
    if (tmpDigitalSendersDic == nil) {
        return nil;
    }
    if (tmpDigitalSendersDic) {
        tmpDigitalSenders= [[SenderListJSONObject alloc] initWithDictionary:tmpDigitalSendersDic withError:error];
        if (*error) {
            return nil;
        }
    }
    return tmpDigitalSenders;
}

- (SenderList2JSONObject *)senderList2InDigitalSendersAtIndex:(NSUInteger)index withError:(NSError **)error
{
    NSDictionary *tmpDigitalSendersDic = [APIParser dictionaryFromResponseArray:self.digitalSenders atIndex:index acceptNil:YES error:error];
    if (*error) {
        return nil;
    }
    SenderList2JSONObject *tmpDigitalSenders = nil;
    if (tmpDigitalSendersDic == nil) {
        return nil;
    }
    if (tmpDigitalSendersDic) {
        tmpDigitalSenders= [[SenderList2JSONObject alloc] initWithDictionary:tmpDigitalSendersDic withError:error];
        if (*error) {
            return nil;
        }
    }
    return tmpDigitalSenders;
}

- (NSNumber *)numberInDigitalSendersAtIndex:(NSUInteger)index withError:(NSError **)error
{
    NSNumber *tmpDigitalSenders = [APIParser numberFromResponseArray:self.digitalSenders atIndex:index acceptNil:YES error:error];
    if (*error) {
        return nil;
    }
    return tmpDigitalSenders;
}

- (NSString *)stringInDigitalSendersAtIndex:(NSUInteger)index withError:(NSError **)error
{
    NSString *tmpDigitalSenders = [APIParser stringFromResponseArray:self.digitalSenders atIndex:index acceptNil:YES error:error];
    if (*error) {
        return nil;
    }
    return tmpDigitalSenders;
}

- (BOOL)booleanInDigitalSendersAtIndex:(NSUInteger)index withError:(NSError **)error
{
    BOOL tmpDigitalSenders = [APIParser boolFromResponseArray:self.digitalSenders atIndex:index acceptNil:YES error:error];
    if (*error) {
        return nil;
    }
    return tmpDigitalSenders;
}

- (NSDate *)dateInDigitalSendersAtIndex:(NSUInteger)index withError:(NSError **)error
{
    NSDate *tmpDigitalSenders = [APIParser dateWithTimeIntervalFromResponseArray:self.digitalSenders atIndex:index acceptNil:YES error:error];
    if (*error) {
        return nil;
    }
    return tmpDigitalSenders;
}

- (NSData *)dataInDigitalSendersAtIndex:(NSUInteger)index withError:(NSError **)error
{
    NSData *tmpDigitalSenders = [APIParser dataFromResponseArray:self.digitalSenders atIndex:index acceptNil:YES error:error];
    if (*error) {
        return nil;
    }
    return tmpDigitalSenders;
}

- (SenderListJSONObject *)senderListInHDOptionsAtIndex:(NSUInteger)index withError:(NSError **)error
{
    NSDictionary *tmpHDOptionsDic = [APIParser dictionaryFromResponseArray:self.HDOptions atIndex:index acceptNil:YES error:error];
    if (*error) {
        return nil;
    }
    SenderListJSONObject *tmpHDOptions = nil;
    if (tmpHDOptionsDic == nil) {
        return nil;
    }
    if (tmpHDOptionsDic) {
        tmpHDOptions= [[SenderListJSONObject alloc] initWithDictionary:tmpHDOptionsDic withError:error];
        if (*error) {
            return nil;
        }
    }
    return tmpHDOptions;
}

- (SenderList2JSONObject *)senderList2InHDOptionsAtIndex:(NSUInteger)index withError:(NSError **)error
{
    NSDictionary *tmpHDOptionsDic = [APIParser dictionaryFromResponseArray:self.HDOptions atIndex:index acceptNil:YES error:error];
    if (*error) {
        return nil;
    }
    SenderList2JSONObject *tmpHDOptions = nil;
    if (tmpHDOptionsDic == nil) {
        return nil;
    }
    if (tmpHDOptionsDic) {
        tmpHDOptions= [[SenderList2JSONObject alloc] initWithDictionary:tmpHDOptionsDic withError:error];
        if (*error) {
            return nil;
        }
    }
    return tmpHDOptions;
}

- (NSString *)stringInDTVHighlightsAtIndex:(NSUInteger)index withError:(NSError **)error
{
    NSString *tmpDTVHighlights = [APIParser stringFromResponseArray:self.DTVHighlights atIndex:index acceptNil:YES error:error];
    if (*error) {
        return nil;
    }
    return tmpDTVHighlights;
}

- (NSString *)titleStringInDTVHighlightsAtIndex:(NSUInteger)index withError:(NSError **)error
{
    NSString *tmpDTVHighlights = [APIParser stringFromResponseArray:self.DTVHighlights atIndex:index acceptNil:YES error:error];
    if (*error) {
        return nil;
    }
    if (tmpDTVHighlights.length > 20) {
        NSDictionary *userInfo = [NSDictionary dictionaryWithObjectsAndKeys:@"titleString", @"propertyName", @"titleString", @"key", @"validation error", @"reason", NSStringFromClass([self class]), @"objectClass",nil];
        *error = [NSError errorWithDomain:kErrorDomain_parser code:kErrorDomain_parser_valueIsNotValid userInfo:userInfo];
        NSLog(@"%@", *error);
        return nil;
    }
    if (tmpDTVHighlights.length < 10) {
        NSDictionary *userInfo = [NSDictionary dictionaryWithObjectsAndKeys:@"titleString", @"propertyName", @"titleString", @"key", @"validation error", @"reason", NSStringFromClass([self class]), @"objectClass",nil];
        *error = [NSError errorWithDomain:kErrorDomain_parser code:kErrorDomain_parser_valueIsNotValid userInfo:userInfo];
        NSLog(@"%@", *error);
        return nil;
    }
    if (tmpDTVHighlights && [tmpDTVHighlights matchesRegExString:@"[a-z0-9]:10"] == NO) {
        NSDictionary *userInfo = [NSDictionary dictionaryWithObjectsAndKeys:@"titleString", @"propertyName", @"titleString", @"key", @"validation error", @"reason", NSStringFromClass([self class]), @"objectClass",nil];
        *error = [NSError errorWithDomain:kErrorDomain_parser code:kErrorDomain_parser_valueIsNotValid userInfo:userInfo];
        NSLog(@"%@", *error);
        return nil;
    }
    return tmpDTVHighlights;
}

- (id)objectInIPTVSendersAtIndex:(NSUInteger)index withError:(NSError **)error
{
    id tmpIPTVSenders = [APIParser objectFromResponseArray:self.IPTVSenders atIndex:index acceptNil:YES error:error];
    if (*error) {
        return nil;
    }
    return tmpIPTVSenders;
}

#pragma mark - NSCoding

- (void)encodeWithCoder:(NSCoder*)coder
{
    [super encodeWithCoder:coder];
    [coder encodeObject:self.digitalSenders forKey:@"digitalSenders"];
    [coder encodeObject:self.HDOptions forKey:@"HDOptions"];
    [coder encodeObject:self.DTVHighlights forKey:@"DTVHighlights"];
    [coder encodeObject:self.IPTVSenders forKey:@"IPTVSenders"];
}
- (id)initWithCoder:(NSCoder *)coder
{
    self = [super initWithCoder:coder];
    self.digitalSenders = [coder decodeObjectForKey:@"digitalSenders"];
    self.HDOptions = [coder decodeObjectForKey:@"HDOptions"];
    self.DTVHighlights = [coder decodeObjectForKey:@"DTVHighlights"];
    self.IPTVSenders = [coder decodeObjectForKey:@"IPTVSenders"];
    return self;
}

#pragma mark - Object Info
- (NSDictionary *)propertyDictionary
{
    NSMutableDictionary *dic = [[NSMutableDictionary alloc] init];
    if (self.digitalSenders) {
        [dic setObject:self.digitalSenders forKey:@"digitalSenders"];
    }
    if (self.HDOptions) {
        [dic setObject:self.HDOptions forKey:@"HDOptions"];
    }
    if (self.DTVHighlights) {
        [dic setObject:self.DTVHighlights forKey:@"DTVHighlights"];
    }
    if (self.IPTVSenders) {
        [dic setObject:self.IPTVSenders forKey:@"IPTVSenders"];
    }
    return dic;
}
- (NSString *)description
{
    return [[self propertyDictionary] description];
}

@end
