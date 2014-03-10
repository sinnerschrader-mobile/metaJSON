
//
//  Created by MetaJSONParser.
//  Copyright (c) _YEAR_ SinnerSchrader Mobile. All rights reserved.
//

#import "_PREFIX_APIParser.h"

NSInteger const k_PREFIX_ErrorDomain_parser_protocolError = 1;
NSInteger const k_PREFIX_ErrorDomain_parser_dictionaryExpected = 2;
NSInteger const k_PREFIX_ErrorDomain_parser_arrayExpected = 3;
NSInteger const k_PREFIX_ErrorDomain_parser_numberExpected = 4;
NSInteger const k_PREFIX_ErrorDomain_parser_stringExpected = 5;
NSInteger const k_PREFIX_ErrorDomain_parser_dateExpected = 6;
NSInteger const k_PREFIX_ErrorDomain_parser_keyNotFound = 7;
NSInteger const k_PREFIX_ErrorDomain_parser_indexNotFound = 8;
NSInteger const k_PREFIX_ErrorDomain_parser_valueIsNull = 9;
NSInteger const k_PREFIX_ErrorDomain_parser_dataExpected = 10;
NSInteger const k_PREFIX_ErrorDomain_parser_valueIsNotValid = 11;

NSString * const k_PREFIX_ErrorDomain_parser = @"_PREFIX_Parser";

NSString * const k_PREFIX_ErrorDomain_parser_userInfoKey = @"_PREFIX_ParserAttributeName";
NSString * const k_PREFIX_ErrorDomain_parser_userInfoValue = @"_PREFIX_ParserAttributeValue";

#ifndef _PREFIX__ASSURE_ERROR
#define _PREFIX__ASSURE_ERROR(error)                                              \
if (!(error)) (error) = (NSError*__autoreleasing*)alloca(sizeof(NSError*));                       \
*(error) = nil;
#endif

@implementation _PREFIX_APIParser

#pragma mark - respone parsing

//date Parsing
+(NSString *)iso8601StringFromDate:(NSDate *)date {
    static NSDateFormatter *    iso8601DateFormatter;
    
    // If the date formatters aren't already set up, do that now and cache them
    // for subsequence reuse.
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        iso8601DateFormatter = [[NSDateFormatter alloc] init];
        
        // TODO: use the system locale! Also, adapt the documentation in the declaration.
        NSLocale *enUSPOSIXLocale = [[NSLocale alloc] initWithLocaleIdentifier:@"en_US_POSIX"];
        [iso8601DateFormatter setLocale:enUSPOSIXLocale];
#if !__has_feature(objc_arc)
        [enUSPOSIXLocale release];
#endif
        // !!!: Adapt the documentation if the format string is modified.
        [iso8601DateFormatter setDateFormat:@"yyyy'-'MM'-'dd'T'HH':'mm':'ssZZZ'"];
    });
    
    if (!date) {
        return nil;
    }
    
    return [iso8601DateFormatter stringFromDate:date];
}

+(NSDate *)dateFromISO8601String:(NSString *)timeString error:(NSError**)error {
    _PREFIX__ASSURE_ERROR(error);
    
    static NSDateFormatter *    iso8601DateFormatter;
    
    // If the date formatters aren't already set up, do that now and cache them
    // for subsequent reuse.
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        iso8601DateFormatter = [[NSDateFormatter alloc] init];
        NSLocale *enUSPOSIXLocale = [[NSLocale alloc] initWithLocaleIdentifier:@"en_US_POSIX"];
        [iso8601DateFormatter setLocale:enUSPOSIXLocale];
#if !__has_feature(objc_arc)
        [enUSPOSIXLocale release];
#endif
        //        [iso8601DateFormatter setDateFormat:@"yyyy'-'MM'-'dd'T'HH':'mm':'ss'+00:00'"];
        //        [iso8601DateFormatter setTimeZone:[NSTimeZone timeZoneForSecondsFromGMT:0]];
        [iso8601DateFormatter setDateFormat:@"yyyy-MM-dd'T'HHmmssZZZ"];
    });
    
    if (!timeString) {
        return nil;
    }
    
    timeString = [timeString stringByReplacingOccurrencesOfString:@":" withString:@""];
    NSDate *date = [iso8601DateFormatter dateFromString:timeString];
    if (!date) {
        *error = [NSError errorWithDomain:k_PREFIX_ErrorDomain_parser code:k_PREFIX_ErrorDomain_parser_dateExpected userInfo:nil];
        return nil;
    }
    
    return date;
}

+(id)objectFromResponseArray:(id)responseObject
                     atIndex:(NSUInteger)index
                   acceptNil:(BOOL)acceptNil
                       error:(NSError**)error {
    _PREFIX__ASSURE_ERROR(error);
    
    if (![responseObject isKindOfClass:[NSArray class]])
    {
        *error = [NSError errorWithDomain:k_PREFIX_ErrorDomain_parser code:k_PREFIX_ErrorDomain_parser_arrayExpected userInfo:nil];
        return nil;
    }
    NSArray *responseArray = (NSArray*)responseObject;
    
    if (index >= [responseArray count]) {
        if (!acceptNil) {
            *error =[NSError errorWithDomain:k_PREFIX_ErrorDomain_parser code:k_PREFIX_ErrorDomain_parser_indexNotFound userInfo:nil];
        }
        return nil;
    }
    
    id object = [responseArray objectAtIndex:index];
    if (!object || object == [NSNull null]) {
        if (!acceptNil) {
            *error =[NSError errorWithDomain:k_PREFIX_ErrorDomain_parser code:k_PREFIX_ErrorDomain_parser_valueIsNull userInfo:nil];
        }
        return nil;
    }
    
    return object;
}

+(NSDictionary*)dictionaryFromResponseArray:(id)responseObject
                                    atIndex:(NSUInteger)index
                                  acceptNil:(BOOL)acceptNil
                                      error:(NSError**)error {
    _PREFIX__ASSURE_ERROR(error);
    
    id dictionary = [self objectFromResponseArray:responseObject atIndex:index acceptNil:acceptNil error:error];
    if (*error || !dictionary)
    {
        // pass unchanged error from objectFromResponseDictionary
        return nil;
    }
    
    if (![dictionary isKindOfClass:[NSDictionary class]])
    {
        *error = [NSError errorWithDomain:k_PREFIX_ErrorDomain_parser code:k_PREFIX_ErrorDomain_parser_dictionaryExpected userInfo:nil];
        return nil;
    }
    
    return (NSDictionary*)dictionary;
}

+(NSArray*)arrayFromResponseArray:(id)responseObject
                          atIndex:(NSUInteger)index
                        acceptNil:(BOOL)acceptNil
                            error:(NSError**)error {
    _PREFIX__ASSURE_ERROR(error);
    
    id array = [self objectFromResponseArray:responseObject atIndex:index acceptNil:acceptNil error:error];
    
    if (*error || !array)
    {
        // pass unchanged error from objectFromResponseDictionary
        return nil;
    }
    
    if (![array isKindOfClass:[NSArray class]])
    {
        *error = [NSError errorWithDomain:k_PREFIX_ErrorDomain_parser code:k_PREFIX_ErrorDomain_parser_arrayExpected userInfo:nil];
        return nil;
    }
    
    return (NSArray*)array;
}

+(NSString *)stringFromResponseArray:(id)responseObject
                             atIndex:(NSUInteger)index
                           acceptNil:(BOOL)acceptNil
                               error:(NSError**)error {
    _PREFIX__ASSURE_ERROR(error);
    
    id string = [self objectFromResponseArray:responseObject atIndex:index acceptNil:acceptNil error:error];
    
    if (*error || !string)
    {
        // pass unchanged error from objectFromResponseDictionary
        return nil;
    }
    
    if (![string isKindOfClass:[NSString class]])
    {
        *error = [NSError errorWithDomain:k_PREFIX_ErrorDomain_parser code:k_PREFIX_ErrorDomain_parser_stringExpected userInfo:nil];
        return nil;
    }
    
    return (NSString*)string;
}

+(NSNumber *)numberFromResponseArray:(id)responseObject
                             atIndex:(NSUInteger)index
                           acceptNil:(BOOL)acceptNil
                               error:(NSError**)error {
    _PREFIX__ASSURE_ERROR(error);
    
    id number = [self objectFromResponseArray:responseObject atIndex:index acceptNil:acceptNil error:error];
    
    if (*error || !number)
    {
        // pass unchanged error from objectFromResponseDictionary
        return nil;
    }
    
    if ([number isKindOfClass:[NSString class]]) {
        
        NSString *numberString = (NSString *)number;
#if !__has_feature(objc_arc)
        NSNumberFormatter * formatter = [[[NSNumberFormatter alloc] init] autorelease];
#else
        NSNumberFormatter * formatter = [[NSNumberFormatter alloc] init];
#endif
        [formatter setNumberStyle:NSNumberFormatterNoStyle];
        number = [formatter numberFromString:numberString];
        
    }
    
    if (![number isKindOfClass:[NSNumber class]])
    {
        *error = [NSError errorWithDomain:k_PREFIX_ErrorDomain_parser code:k_PREFIX_ErrorDomain_parser_numberExpected userInfo:nil];
        return nil;
    }
    
    NSNumber *_PREFIX_Number = [NSNumber numberWithLongLong:[number longLongValue]];
    return (NSNumber*)_PREFIX_Number;
}

+(BOOL)boolFromResponseArray:(id)responseObject
                     atIndex:(NSUInteger)index
                   acceptNil:(BOOL)acceptNil
                       error:(NSError**)error {
    _PREFIX__ASSURE_ERROR(error);
    
    NSNumber *number = [self numberFromResponseArray:responseObject atIndex:index acceptNil:acceptNil error:error];
    
    if (*error || !number)
    {
        // pass unchanged error from objectFromResponseDictionary
        return NO;
    }
    
    return [number boolValue];
}

+(NSDate *)dateWithTimeIntervalFromResponseArray:(id)responseObject
                                         atIndex:(NSUInteger)index
                                       acceptNil:(BOOL)acceptNil
                                           error:(NSError**)error {
    _PREFIX__ASSURE_ERROR(error);
    
    NSNumber *timeInterval = [self numberFromResponseArray:responseObject atIndex:index acceptNil:acceptNil error:error];
    
    if (*error || !timeInterval || ![timeInterval isKindOfClass:[NSNumber class]])
    {
        // pass unchanged error from stringFromResponseDictionary
        *error = [NSError errorWithDomain:k_PREFIX_ErrorDomain_parser code:k_PREFIX_ErrorDomain_parser_dateExpected userInfo:nil];
        return nil;
    }
    
    NSDate *date = [NSDate dateWithTimeIntervalSince1970:[timeInterval doubleValue]];
    
    return date;
}

+ (NSData*)dataFromResponseArray:(NSDictionary*)responseObject
                         atIndex:(NSUInteger)index
                       acceptNil:(BOOL)acceptNil
                           error:(NSError**)error
{
    _PREFIX__ASSURE_ERROR(error);
    
    id data = [self objectFromResponseArray:responseObject atIndex:index acceptNil:acceptNil error:error];
    
    if (*error || !data)
    {
        // pass unchanged error from objectFromResponseDictionary
        return nil;
    }
    
    if ([data isKindOfClass:[NSString class]]) {
        NSString *dataString = (NSString *)data;
        data = [dataString dataUsingEncoding:NSUTF8StringEncoding];
    }
    
    if (![data isKindOfClass:[NSData class]]) {
        *error = [NSError errorWithDomain:k_PREFIX_ErrorDomain_parser code:k_PREFIX_ErrorDomain_parser_dataExpected userInfo:nil];
        return nil;
    }
    
    return (NSData*)data;
}

+(id)objectFromResponseDictionary:(id)responseObject
                           forKey:(NSString*)key
                        acceptNil:(BOOL)acceptNil
                            error:(NSError**)error
{
    _PREFIX__ASSURE_ERROR(error);
    
    if (![responseObject isKindOfClass:[NSDictionary class]])
    {
        *error = [NSError errorWithDomain:k_PREFIX_ErrorDomain_parser code:k_PREFIX_ErrorDomain_parser_dictionaryExpected userInfo:nil];
        return nil;
    }
    NSDictionary *responseDict = responseObject;
    
    id object = [responseDict objectForKey:key];
    if (!object) {
        if (!acceptNil) {
            *error =[NSError errorWithDomain:k_PREFIX_ErrorDomain_parser code:k_PREFIX_ErrorDomain_parser_keyNotFound userInfo:@{k_PREFIX_ErrorDomain_parser_userInfoKey: key}];
        }
        return nil;
    }
    if (object == [NSNull null]) {
        if (!acceptNil) {
            *error =[NSError errorWithDomain:k_PREFIX_ErrorDomain_parser code:k_PREFIX_ErrorDomain_parser_valueIsNull userInfo:@{k_PREFIX_ErrorDomain_parser_userInfoKey: key}];
        }
        return nil;
    }
    
    return object;
}

+(NSDictionary*)dictionaryFromResponseDictionary:(id)responseObject
                                          forKey:(NSString*)key
                                       acceptNil:(BOOL)acceptNil
                                           error:(NSError**)error
{
    _PREFIX__ASSURE_ERROR(error);
    
    id dictionary = [self objectFromResponseDictionary:responseObject
                                                forKey:key
                                             acceptNil:acceptNil
                                                 error:error];
    if (*error || !dictionary)
    {
        // pass unchanged error from objectFromResponseDictionary
        return nil;
    }
    
    if (![dictionary isKindOfClass:[NSDictionary class]])
    {
        *error = [NSError errorWithDomain:k_PREFIX_ErrorDomain_parser code:k_PREFIX_ErrorDomain_parser_dictionaryExpected userInfo:nil];
        return nil;
    }
    
    return (NSDictionary*)dictionary;
}

+(NSArray*)arrayFromResponseDictionary:(id)responseObject
                                forKey:(NSString*)key
                             acceptNil:(BOOL)acceptNil
                                 error:(NSError**)error
{
    _PREFIX__ASSURE_ERROR(error);
    
    id array = [self objectFromResponseDictionary:responseObject
                                           forKey:key
                                        acceptNil:acceptNil
                                            error:error];
    if (*error || !array)
    {
        // pass unchanged error from objectFromResponseDictionary
        return nil;
    }
    
    if (![array isKindOfClass:[NSArray class]])
    {
        *error = [NSError errorWithDomain:k_PREFIX_ErrorDomain_parser code:k_PREFIX_ErrorDomain_parser_arrayExpected userInfo:nil];
        return nil;
    }
    
    return (NSArray*)array;
}

+(NSNumber*)numberFromResponseDictionary:(id)responseObject
                                  forKey:(NSString*)key
                               acceptNil:(BOOL)acceptNil
                                   error:(NSError**)error
{
    _PREFIX__ASSURE_ERROR(error);
    
    id number = [self objectFromResponseDictionary:responseObject
                                            forKey:key
                                         acceptNil:acceptNil
                                             error:error];
    if (*error || !number)
    {
        // pass unchanged error from objectFromResponseDictionary
        return nil;
    }

    if ([number isKindOfClass:[NSNumber class]]) {
        return number;
    }

    if ([number isKindOfClass:[NSString class]]) {
        
        NSString *numberString = (NSString *)number;
        
#if !__has_feature(objc_arc)
        NSNumberFormatter * formatter = [[[NSNumberFormatter alloc] init] autorelease];
#else
        NSNumberFormatter * formatter = [[NSNumberFormatter alloc] init];
#endif
        [formatter setNumberStyle:NSNumberFormatterNoStyle];
        number = [formatter numberFromString:numberString];
        
    }
    
    if (![number isKindOfClass:[NSNumber class]])
    {
        *error = [NSError errorWithDomain:k_PREFIX_ErrorDomain_parser code:k_PREFIX_ErrorDomain_parser_numberExpected userInfo:nil];
        return nil;
    }
    
    NSNumber *_PREFIX_Number = [NSNumber numberWithLongLong:[number longLongValue]];
    return (NSNumber*)_PREFIX_Number;
}

+(BOOL)boolFromResponseDictionary:(id)responseObject
                           forKey:(NSString*)key
                        acceptNil:(BOOL)acceptNil
                            error:(NSError**)error {
    _PREFIX__ASSURE_ERROR(error);
    
    NSNumber *number = [self numberFromResponseDictionary:responseObject
                                                   forKey:key
                                                acceptNil:acceptNil
                                                    error:error];
    if (*error || !number)
    {
        // pass unchanged error from objectFromResponseDictionary
        return NO;
    }
    
    return [number boolValue];
}

+(NSString*)stringFromResponseDictionary:(id)responseObject
                                  forKey:(NSString*)key
                            acceptNumber:(BOOL)acceptNumber
                               acceptNil:(BOOL)acceptNil
                                   error:(NSError**)error
{
    _PREFIX__ASSURE_ERROR(error);
    
    id string = [self objectFromResponseDictionary:responseObject
                                            forKey:key
                                         acceptNil:acceptNil
                                             error:error];
    if (*error || !string)
    {
        // pass unchanged error from objectFromResponseDictionary
        return nil;
    }
    
    if (acceptNumber && [string isKindOfClass:[NSNumber class]]) {
        string = [string description];
    }
    
    if (![string isKindOfClass:[NSString class]])
    {
        *error = [NSError errorWithDomain:k_PREFIX_ErrorDomain_parser code:k_PREFIX_ErrorDomain_parser_stringExpected userInfo:nil];
        return nil;
    }
    
    return (NSString*)string;
}

+(NSDate*)dateFromResponseDictionary:(id)responseObject
                              forKey:(NSString*)key
                           acceptNil:(BOOL)acceptNil
                               error:(NSError**)error
{
    _PREFIX__ASSURE_ERROR(error);
    
    id dateObject = [self stringFromResponseDictionary:responseObject
                                                forKey:key
                                          acceptNumber:YES
                                             acceptNil:acceptNil
                                                 error:error];
    if (*error || !dateObject)
    {
        // pass unchanged error from stringFromResponseDictionary
        return nil;
    }
    
    NSDate *date = nil;
    if ([dateObject isKindOfClass:[NSString class]]) {
        NSString *dateString = (NSString *)dateObject;
        date = [self dateFromISO8601String:dateString error:error];
        if (*error) {
            return nil;
        }
    } else {
        NSNumber *dateNumber = (NSNumber *)dateObject;
        date = [NSDate dateWithTimeIntervalSince1970:[dateNumber longValue]];
    }
    
    return date;
}

+ (NSData*)dataFromResponseDictionary:(NSDictionary*)responseObject
                               forKey:(NSString*)key
                            acceptNil:(BOOL)acceptNil
                                error:(NSError**)error
{
    _PREFIX__ASSURE_ERROR(error);
    
    id data = [self objectFromResponseDictionary:responseObject
                                          forKey:key
                                       acceptNil:acceptNil
                                           error:error];
    if (*error || !data)
    {
        // pass unchanged error from objectFromResponseDictionary
        return nil;
    }
    
    if ([data isKindOfClass:[NSString class]]) {
        NSString *dataString = (NSString *)data;
        data = [dataString dataUsingEncoding:NSUTF8StringEncoding];
    }
    
    if (![data isKindOfClass:[NSData class]]) {
        *error = [NSError errorWithDomain:k_PREFIX_ErrorDomain_parser code:k_PREFIX_ErrorDomain_parser_dataExpected userInfo:nil];
        return nil;
    }
    
    return (NSData*)data;
}


+(NSDate*)dateWithTimeIntervalFromResponseDictionary:(id)responseObject
                                              forKey:(NSString*)key
                                           acceptNil:(BOOL)acceptNil
                                               error:(NSError**)error
{
    _PREFIX__ASSURE_ERROR(error);
    
    NSNumber *timeInterval = [self numberFromResponseDictionary:responseObject
                                                         forKey:key
                                                      acceptNil:acceptNil
                                                          error:error];
    if (!timeInterval && acceptNil) {
        return nil;
    }
    
    if (*error || !timeInterval || ![timeInterval isKindOfClass:[NSNumber class]])
    {
        // pass unchanged error from stringFromResponseDictionary
        *error = [NSError errorWithDomain:k_PREFIX_ErrorDomain_parser code:k_PREFIX_ErrorDomain_parser_dateExpected userInfo:nil];
        return nil;
    }
    
    NSDate *date = [NSDate dateWithTimeIntervalSince1970:[timeInterval doubleValue]];
    
    return date;
}

+(NSDate*)dateWithMilliSecondsTimeIntervalFromResponseDictionary:(id)responseObject
                                                          forKey:(NSString*)key
                                                       acceptNil:(BOOL)acceptNil
                                                           error:(NSError**)error
{
    _PREFIX__ASSURE_ERROR(error);
    
    NSNumber *dateNumber = [self numberFromResponseDictionary:responseObject
                                                       forKey:key
                                                    acceptNil:acceptNil
                                                        error:error];
    if (!dateNumber && acceptNil) {
        return nil;
    }
    
    NSNumber *timeInterval = [NSNumber numberWithDouble:(dateNumber.doubleValue / 1000)];
    
    if (*error || !timeInterval || ![timeInterval isKindOfClass:[NSNumber class]])
    {
        // pass unchanged error from stringFromResponseDictionary
        *error = [NSError errorWithDomain:k_PREFIX_ErrorDomain_parser code:k_PREFIX_ErrorDomain_parser_dateExpected userInfo:nil];
        return nil;
    }
    
    NSDate *date = [NSDate dateWithTimeIntervalSince1970:[timeInterval doubleValue]];
    
    return date;
}


@end
