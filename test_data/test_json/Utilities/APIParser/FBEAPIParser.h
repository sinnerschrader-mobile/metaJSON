
//
//  Created by MetaJSONParser.
//  Copyright (c) 2013 SinnerSchrader Mobile. All rights reserved.
//

#import <Foundation/Foundation.h>

extern NSInteger const kFBEErrorDomain_parser_protocolError;
extern NSInteger const kFBEErrorDomain_parser_dictionaryExpected;
extern NSInteger const kFBEErrorDomain_parser_arrayExpected;
extern NSInteger const kFBEErrorDomain_parser_numberExpected;
extern NSInteger const kFBEErrorDomain_parser_stringExpected;
extern NSInteger const kFBEErrorDomain_parser_dateExpected;
extern NSInteger const kFBEErrorDomain_parser_keyNotFound;
extern NSInteger const kFBEErrorDomain_parser_indexNotFound;
extern NSInteger const kFBEErrorDomain_parser_valueIsNull;
extern NSInteger const kFBEErrorDomain_parser_dataExpected;
extern NSInteger const kFBEErrorDomain_parser_valueIsNotValid;

extern NSString * const kFBEErrorDomain_parser;

/**
	The APIParser facilitates parsing the fields of the JSON response.
 
	The ResponseObjects may be `NSDictionaries` or `NSArrays`, depending on the method. Each method performs type checking and returns an sets the `NSError` indirect reference to an `NSError` object. The `NSError` indirect reference will be guaranteed to be `nil` upon success, which is contrary to Cocoa conventions but necessary since `nil` or `FALSE` may be valid return values.
 */
@interface FBEAPIParser : NSObject

#pragma mark - Response Parsing

/**
 Gets an `NSDictionary` object from the response array.
 @param responseObject The JSON Array
 @param key The key of the item of the responseObject to be read
 @param acceptNil If set to YES, no error will be given if the item to be read is not available. Otherwise, an NSError is generated.
 @param error `nil` if parsing was successful
 @returns The dictionary read from the responseObject
 */
+(NSDictionary*)dictionaryFromResponseArray:(id)responseObject
                                    atIndex:(NSUInteger)index
                                  acceptNil:(BOOL)acceptNil
                                      error:(NSError**)error;

/**
 Gets an `NSArray` object from the response array.
 @param responseObject The JSON Array
 @param key The key of the item of the responseObject to be read
 @param acceptNil If set to YES, no error will be given if the item to be read is not available. Otherwise, an NSError is generated.
 @param error `nil` if parsing was successful
 @returns The array read from the responseObject
 */
+(NSArray*)arrayFromResponseArray:(id)responseObject
                          atIndex:(NSUInteger)index
                        acceptNil:(BOOL)acceptNil
                            error:(NSError**)error;

/**
 Gets an `NSString` object from the response array.
 @param responseObject The JSON Array
 @param key The key of the item of the responseObject to be read
 @param acceptNil If set to YES, no error will be given if the item to be read is not available. Otherwise, an NSError is generated.
 @param error `nil` if parsing was successful
 @returns The string read from the responseObject
 */

+(NSString *)stringFromResponseArray:(id)responseObject
                             atIndex:(NSUInteger)index
                           acceptNil:(BOOL)acceptNil
                               error:(NSError**)error;

/**
 Gets an `NSNumber` object from the response array.
 @param responseObject	The JSON Array
 @param key				The key of the item of the responseObject to be read
 @param acceptNil		If set to YES, no error will be given if the item to be read is not available. Otherwise, an NSError is generated.
 @param error			`nil` if parsing was successful
 @returns				The object read from the responseObject
 */
+(NSNumber *)numberFromResponseArray:(id)responseObject
                             atIndex:(NSUInteger)index
                           acceptNil:(BOOL)acceptNil
                               error:(NSError**)error;

/**
 Gets a `BOOL` value from the response array.
 @param responseObject The JSON Array
 @param key The key of the item of the responseObject to be read
 @param acceptNil If set to YES, no error will be given if the item to be read is not available. Otherwise, an NSError is generated.
 @param error `nil` if parsing was successful
 @returns The value read from the responseObject. Will be `NO` if the item to be read is not available.
 */
+(BOOL)boolFromResponseArray:(id)responseObject
                     atIndex:(NSUInteger)index
                   acceptNil:(BOOL)acceptNil
                       error:(NSError**)error;

/**
 Gets an `NSDate` object from the response array.
 @param responseObject The JSON Array
 @param key The key of the item of the responseObject to be read (the value for this key should be time interval since 1970)
 @param acceptNil If set to YES, no error will be given if the item to be read is not available. Otherwise, an NSError is generated.
 @param error `nil` if parsing was successful
 @returns The date read from the responseObject
 */
+(NSDate *)dateWithTimeIntervalFromResponseArray:(id)responseObject
                                         atIndex:(NSUInteger)index
                                       acceptNil:(BOOL)acceptNil
                                           error:(NSError**)error;



/**
 Gets an `NSData` object from the response array.
 @param responseObject The JSON Array
 @param key The key of the item of the responseObject to be read
 @param acceptNil If set to YES, no error will be given if the item to be read is not available. Otherwise, an NSError is generated.
 @param error `nil` if parsing was successful
 @returns The data read from the responseObject
 */
+ (NSData*)dataFromResponseArray:(NSDictionary*)responseObject
                         atIndex:(NSUInteger)index
                       acceptNil:(BOOL)acceptNil
                           error:(NSError**)error;

/**
	Gets an Objective-C object of an anonymous type from the response object.
	@param responseObject	The JSON Dictionary
	@param key				The key of the item of the responseObject to be read
	@param acceptNil		If set to YES, no error will be given if the item to be read is not available. Otherwise, an NSError is generated.
	@param error			`nil` if parsing was successful
	@returns				The object read from the responseObject
 */
+(id)objectFromResponseDictionary:(id)responseObject
                           forKey:(NSString*)key
                        acceptNil:(BOOL)acceptNil
                            error:(NSError**)error;


/**
	Gets an Objective-C object of an anonymous type from the response array.
	@param responseObject	The JSON Array
	@param index			The index of the item of the responseObject to be read
	@param acceptNil		If set to YES, no error will be given if the item to be read is not available. Otherwise, an NSError is generated.
	@param error			`nil` if parsing was successful
	@returns				The object read from the responseObject
 */
+(id)objectFromResponseArray:(id)responseObject
                     atIndex:(NSUInteger)index
                   acceptNil:(BOOL)acceptNil
                       error:(NSError**)error;


/**
	Gets an `NSNumber` object from the response object.
	@param responseObject	The JSON Dictionary
	@param key				The key of the item of the responseObject to be read
	@param acceptNil		If set to YES, no error will be given if the item to be read is not available. Otherwise, an NSError is generated.
	@param error			`nil` if parsing was successful
	@returns				The object read from the responseObject
 */
+(NSNumber*)numberFromResponseDictionary:(id)responseObject
                                  forKey:(NSString*)key
                               acceptNil:(BOOL)acceptNil
                                   error:(NSError**)error;


/**
	Gets a `BOOL` value from the response object.
	@param responseObject The JSON Dictionary
	@param key The key of the item of the responseObject to be read
	@param acceptNil If set to YES, no error will be given if the item to be read is not available. Otherwise, an NSError is generated.
	@param error `nil` if parsing was successful
	@returns The value read from the responseObject. Will be `NO` if the item to be read is not available.
 */
+(BOOL)boolFromResponseDictionary:(id)responseObject
						   forKey:(NSString*)key
						acceptNil:(BOOL)acceptNil
							error:(NSError**)error
;

/**
	Gets an `NSDictionary` object from the response object.
	@param responseObject The JSON Dictionary
	@param key The key of the item of the responseObject to be read
	@param acceptNil If set to YES, no error will be given if the item to be read is not available. Otherwise, an NSError is generated.
	@param error `nil` if parsing was successful
	@returns The dictionary read from the responseObject
 */
+(NSDictionary*)dictionaryFromResponseDictionary:(id)responseObject
                                          forKey:(NSString*)key
                                       acceptNil:(BOOL)acceptNil
                                           error:(NSError**)error;


/**
	Gets an `NSArray` object from the response object.
	@param responseObject The JSON Dictionary
	@param key The key of the item of the responseObject to be read
	@param acceptNil If set to YES, no error will be given if the item to be read is not available. Otherwise, an NSError is generated.
	@param error `nil` if parsing was successful
	@returns The array read from the responseObject
 */
+(NSArray*)arrayFromResponseDictionary:(id)responseObject
                                forKey:(NSString*)key
                             acceptNil:(BOOL)acceptNil
                                 error:(NSError**)error
;

/**
	Gets an `NSString` object from the response object.
	@param responseObject The JSON Dictionary
	@param key The key of the item of the responseObject to be read
	@param acceptNumber If yes, the string will be generated by invocing -desription on the responseObject if it is kind of an NSNumber.
	@param acceptNil If set to YES, no error will be given if the item to be read is not available. Otherwise, an NSError is generated.
	@param error `nil` if parsing was successful
	@returns The string read from the responseObject
 */
+(NSString*)stringFromResponseDictionary:(id)responseObject
                                  forKey:(NSString*)key
							acceptNumber:(BOOL)acceptNumber
                               acceptNil:(BOOL)acceptNil
                                   error:(NSError**)error
;

/**
	Gets an `NSDate` object from the response object. The JSON data for the `key` may be either an iso8601 date string or a number. In case of a string, the formatting must be `yyyy-MM-dd'T'HHmmssZZZ`; in case of a number it must be a Unix time stamp (since 1970).
	@param responseObject The JSON Dictionary
	@param key The key of the item of the responseObject to be read
	@param acceptNil If set to YES, no error will be given if the item to be read is not available. Otherwise, an NSError is generated.
	@param error `nil` if parsing was successful
	@returns The date read from the responseObject
 */
+(NSDate*)dateFromResponseDictionary:(id)responseObject
                              forKey:(NSString*)key
                           acceptNil:(BOOL)acceptNil
                               error:(NSError**)error
;

/**
 Gets an `NSData` object from the response object.
 @param responseObject The JSON Dictionary
 @param key The key of the item of the responseObject to be read
 @param acceptNil If set to YES, no error will be given if the item to be read is not available. Otherwise, an NSError is generated.
 @param error `nil` if parsing was successful
 @returns The data read from the responseObject
 */
+ (NSData*)dataFromResponseDictionary:(NSDictionary*)responseObject
                               forKey:(NSString*)key
                            acceptNil:(BOOL)acceptNil
                                error:(NSError**)error
;

/**
 Gets an `NSDate` object from the response object.
 @param responseObject The JSON Dictionary
 @param key The key of the item of the responseObject to be read (the value for this key should be time interval since 1970)
 @param acceptNil If set to YES, no error will be given if the item to be read is not available. Otherwise, an NSError is generated.
 @param error `nil` if parsing was successful
 @returns The date read from the responseObject
 */
+(NSDate*)dateWithTimeIntervalFromResponseDictionary:(id)responseObject
                                              forKey:(NSString*)key
                                           acceptNil:(BOOL)acceptNil
                                               error:(NSError**)error
;

/**
 Gets an `NSDate` object from the response object (milliseconds -> seconds).
 @param responseObject The JSON Dictionary
 @param key The key of the item of the responseObject to be read (the value for this key should be time interval since 1970)
 @param acceptNil If set to YES, no error will be given if the item to be read is not available. Otherwise, an NSError is generated.
 @param error `nil` if parsing was successful
 @returns The date read from the responseObject
 */
+(NSDate*)dateWithMilliSecondsTimeIntervalFromResponseDictionary:(id)responseObject
                                                          forKey:(NSString*)key
                                                       acceptNil:(BOOL)acceptNil
                                                           error:(NSError**)error
;


/**
	The `NSString` is generated using a predefined `NSDateFormatter`.
 
 The date formatter is cached after the first invocation.
 The date formatter is currently hardcoded to use the locale `en_US_POSIX`and date format `yyyy'-'MM'-'dd'T'HH':'mm':'ssZZZ'`.
 TODO: This will likely have to change!
	@param date
	@returns The formatted date string
 */
+(NSString*)iso8601StringFromDate:(NSDate *)date;

@end
