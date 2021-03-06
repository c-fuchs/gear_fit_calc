<?php

/*
   Plugin Name: Fit Reports Update
   description: A plugin to take Caldera form submissions and save them to moto_gear_fit_calc.
                Works in conjuction with Caldera Forms, called by hook upon new form submission
   Version: 1.0.3
   Author: Carolanne Fuchs
   Author URI: https://carolannefuchs.com
*/

defined( 'ABSPATH' ) or exit;

//Class on_submit(){
// Upon a new caldera forms submission, plugin should read from caldera's db, then write to the moto gear fit db
// First update fit_reports, then gear, then users, then fetch results

    function fit_report_updater() {
        $servername = "localhost"; //"192.185.4.113"; //need to figure out what the servername actually is, this is remote access host address
        $username = "####";  //your user name for php my admin
        $password = "####";  //password it will probably be empty
        $database1 = "####"; //Caldera form results db name
        $database2 = "####"; //new db name to INSERT INTO

        // Create connection to caldera db
        $conn = new mysqli($servername, $username, $password, $database1);
        // Check connection
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        } 
        echo "Connected successfully";

        // Read new form entries and save as variables
        // Find most recent form entry ID
        $sql = "SELECT entry_id FROM wp_cf_form_entry_values ORDER BY entry_id DESC LIMIT 1";
        if ($result = $conn->query($sql)) {
			while ($row = $result->fetch_assoc()) {
				$entry_id = $row[0];
			}
			echo $entry_id;
		}

        // Get user_bust
        $sql = "SELECT value FROM wp_cf_form_entry_values WHERE entry_id = $entry_id AND slug = user_bust";
		if ($result = $conn->query($sql)) {
			while ($row = $result->fetch_assoc()) {
				$user_bust = $row[0];
			}
			echo $user_bust;
		}
        // Get user_waist
        $sql = "SELECT value FROM wp_cf_form_entry_values WHERE entry_id = $entry_id AND slug = user_waist";
        $result = $conn->query($sql);
        $user_waist = $result[0];
		if ($result = $conn->query($sql)) {
			while ($row = $result->fetch_assoc()) {
				$user_waist = $row[0];
			}
			echo $user_waist;
		}
		
        // If skip (first) fit report does NOT exist, get values
        $sql = "SELECT value FROM wp_cf_form_entry_values WHERE entry_id = $entry_id AND slug = skip_fit_report";
        if ($result = $conn->query($sql)) {
			while ($row = $result->fetch_assoc()) {
				$skip_fit_report = $row[0];
			}
		}    
        if ($skip_fit_report == "skip_fit_report.opt2031062") {
            $fr_skip = True;
            echo "No fit report";
        } else {
			//fetch gear item-specific fit report values
            // Get gear_brand
            $sql = "SELECT value FROM wp_cf_form_entry_values WHERE entry_id = $entry_id AND slug = gear_brand";
            if ($result = $conn->query($sql)) {
				while ($row = $result->fetch_assoc()) {
					$gear_brand = $row[0];
				}
			} 
            // Get gear_name
            $sql = "SELECT value FROM wp_cf_form_entry_values WHERE entry_id = $entry_id AND slug = gear_name";
            if ($result = $conn->query($sql)) {
				while ($row = $result->fetch_assoc()) {
					$gear_name = $row[0];
				}
			}
            // Get gear_size
            $sql = "SELECT value FROM wp_cf_form_entry_values WHERE entry_id = $entry_id AND slug = gear_size";
            if ($result = $conn->query($sql)) {
				while ($row = $result->fetch_assoc()) {
					$gear_size = $row[0];
				}
			}
            // Get back_protector
            $sql = "SELECT value FROM wp_cf_form_entry_values WHERE entry_id = $entry_id AND slug = back_protector";
            if ($result = $conn->query($sql)) {
				while ($row = $result->fetch_assoc()) {
					$fr_backpro = $row[0];
				}
			}
            // Get bust_fit
            $sql = "SELECT value FROM wp_cf_form_entry_values WHERE entry_id = $entry_id AND slug = bust_fit";
            if ($result = $conn->query($sql)) {
				while ($row = $result->fetch_assoc()) {
					$fr_bust_adjust = $row[0];
				}
			}
            // Get waist_fit
            $sql = "SELECT value FROM wp_cf_form_entry_values WHERE entry_id = $entry_id AND slug = waist_fit";
            if ($result = $conn->query($sql)) {
				while ($row = $result->fetch_assoc()) {
					$fr_waist_adjust = $row[0];
				}
			}
        }

        //write new entries to tables in database2
        // Create connection to moto fit db, database2
        $conn = new mysqli($servername, $username, $password, $database2);
        // Check connection
        if ($result = $conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        } 
        echo "Connected successfully";

        // Update users with new user_bust, and user_waist
        $sql = "INSERT INTO fc_users (user_bust) VALUES ($user_bust)";
        if ($result = $conn->query($sql)){
            echo "User bust updated";
        } else {
            echo "Error: " . $sql . "" . mysqli_error($conn);
        } 
        $sql = "INSERT INTO fc_users (user_waist) VALUES ($user_waist)";
        if ($result = $conn->query($sql)){
            echo "User waist updated";
        } else {
            echo "Error: " . $sql . "" . mysqli_error($conn);
        }    

        // Get newest user_id
        $sql = "SELECT user_id FROM fc_users ORDER BY user_id DESC LIMIT 1";
        if ($result = $conn->query($sql)) {
			while ($row = $result->fetch_assoc()) {
				$user_id = $row[0];
			}
		}

        // Get gear_id for first fit report
        $sql = "SELECT gear_id FROM fc_gear WHERE gear_brand = $gear_brand AND gear_name = $gear_name AND gear_size = $gear_size";
        if ($result = $conn->query($sql)) {
			while ($row = $result->fetch_assoc()) {
				$gear_id = $row[0];
			}
		}

        // Insert values into fit_reports for first fit report
        $sql = "INSERT INTO fc_fit_reports VALUES fr_user_id = $user_id, fr_gear_id = $gear_id, fr_backpro = $fr_backpro, fr_bust_adjust = $fr_bust_adjust, fr_waist_adjust = $fr_waist_adjust";
        if ($result = $conn->query($sql)){
            echo "User user_id, gear_id, backpro, bust adj, and waist adj updated";
        } else {
            echo "Error: " . $sql . "" . mysqli_error($conn);
        }
        // Get newest fc_fit_reports fr_id
        $sql = "SELECT fr_id FROM fc_fit_reports ORDER BY fr_id DESC LIMIT 1";
        if ($result = $conn->query($sql)) {
			while ($row = $result->fetch_assoc()) {
				$fr_id = $row[0];
			}
		}

        // Get gear_derived_bust value from gear and save as gear_bust
        $sql = "SELECT gear_derived_bust FROM fc_gear WHERE gear_id = $gear_id";
        if ($result = $conn->query($sql)) {
			while ($row = $result->fetch_assoc()) {
				$gear_bust = $row[0];
			}
		}
        // Get gear_derived_waist value from gear and save as gear_waist
        $sql = "SELECT gear_derived_waist FROM fc_gear WHERE gear_id = $gear_id";
        if ($result = $conn->query($sql)) {
			while ($row = $result->fetch_assoc()) {
				$gear_waist = $row[0];
			}
		}

        // calculate gear_bust_est for this fit report
        $gear_bust_est = ($gear_bust + $user_bust + $fr_bust_adjust + $fr_backpro)/2;

        // calculate gear_waist_est for this fit report
        $gear_waist_est = ($gear_waist + $user_waist + $fr_waist_adjust + ($fr_backpro/2))/2;

        // calculate user_bust_est for this fit report
        $user_bust_est = ($gear_bust_est + $user_bust + $fr_bust_adjust)/2;

        // calculate user_waist_est for this fit report
        $user_waist_est = ($gear_waist_est + $user_waist + $fr_waist_adjust)/2;
            
        // update gear_bust_est in fit_reports table 
        $sql = "UPDATE fc_fit_reports SET (gear_bust_est) = ($gear_bust_est) WHERE fr_id = $fr_id";
        if ($result = $conn->query($sql)){
            echo "Fit reports gear bust updated";
        } else {
            echo "Error: " . $sql . "" . mysqli_error($conn);
        }
        // update gear_waist_est in fit_reports table 
        $sql = "UPDATE fc_fit_reports SET (gear_waist_est) = ($gear_waist_est) WHERE fr_id = $fr_id";
        if ($result = $conn->query($sql)){
            echo "Fit reports gear waist updated";
        } else {
            echo "Error: " . $sql . "" . mysqli_error($conn);
        }

        // update user_bust_est in fit_reports table
        $sql = "UPDATE fc_fit_reports SET user_bust_est = $user_bust_est WHERE fr_id = $fr_id";
        if ($result = $conn->query($sql)){
            echo "Fit reports user bust updated";
        } else {
            echo "Error: " . $sql . "" . mysqli_error($conn);
        }

        // update user_waist_est in fit_reports table
        $sql = "UPDATE fc_fit_reports SET user_waist_est = $user_waist_est WHERE fr_id = $fr_id";    
        if ($result = $conn->query($sql)){
            echo "Fit reports user waist updated";
        } else {
            echo "Error: " . $sql . "" . mysqli_error($conn);
        }

    ;}

fit_report_updater();	

?>
